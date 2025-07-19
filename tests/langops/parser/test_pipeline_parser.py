import unittest
import unittest.mock
import tempfile
import os
from langops.parser.pipeline_parser import PipelineParser
from langops.parser.types.pipeline_types import (
    SeverityLevel,
    StageWindow,
    ParsedPipelineBundle,
)
from langops.parser.registry import ParserRegistry


class TestPipelineParser(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures."""
        self.sample_log_data = """
        INFO: Starting pipeline
        ERROR: Something went wrong
        WARNING: This is a warning
        CRITICAL: Critical error occurred
        """

    def test_init_with_source(self):
        """Test PipelineParser initialization with source parameter."""
        parser = PipelineParser(source="jenkins")
        self.assertEqual(parser.source, "jenkins")
        self.assertIsInstance(parser.patterns, dict)
        self.assertIsInstance(parser.stage_patterns, list)
        self.assertIn("groovy", parser.patterns)

    def test_init_with_config_file(self):
        """Test PipelineParser initialization with config file."""
        yaml_content = """
source: test_pipeline
patterns:
  python:
    - regex: "Error:"
      severity: "ERROR"
    - regex: "Warning:"
      severity: "WARNING"
stage_patterns:
  - "##\\\\[section\\\\]Starting: (.+)"
  - "##\\\\[section\\\\]Finishing: (.+)"
"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(yaml_content)
            f.flush()

            try:
                parser = PipelineParser(config_file=f.name)
                self.assertEqual(parser.source, "test_pipeline")
                self.assertIn("python", parser.patterns)
                self.assertEqual(len(parser.stage_patterns), 2)
            finally:
                os.unlink(f.name)

    def test_init_with_both_source_and_config(self):
        """Test PipelineParser initialization with both source and config file."""
        yaml_content = """
source: custom_source
patterns:
  custom:
    - regex: "CUSTOM_ERROR:"
      severity: "ERROR"
stage_patterns:
  - "CUSTOM_STAGE: (.+)"
"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(yaml_content)
            f.flush()

            try:
                parser = PipelineParser(source="jenkins", config_file=f.name)
                self.assertEqual(
                    parser.source, "custom_source"
                )  # Config file overrides source
                self.assertIn("groovy", parser.patterns)  # From jenkins source
                self.assertIn("custom", parser.patterns)  # From config file
            finally:
                os.unlink(f.name)

    def test_init_with_unknown_source(self):
        """Test PipelineParser initialization with unknown source raises ValueError."""
        with self.assertRaises(ValueError) as cm:
            PipelineParser(source="unknown_source")
        self.assertIn("Unknown source for patterns", str(cm.exception))

    def test_init_with_additional_kwargs(self):
        """Test PipelineParser initialization with additional kwargs."""
        parser = PipelineParser(source="jenkins", window_size=50, custom_param="test")
        self.assertEqual(parser.additional_kwargs["window_size"], 50)
        self.assertEqual(parser.additional_kwargs["custom_param"], "test")

    def test_init_without_source_or_config(self):
        """Test PipelineParser initialization without source or config."""
        parser = PipelineParser()
        self.assertEqual(parser.source, "unknown")
        self.assertEqual(parser.patterns, {})
        self.assertEqual(parser.stage_patterns, [])

    def test_parse_basic(self):
        """Test basic parsing functionality."""
        parser = PipelineParser(source="jenkins")
        log_data = """
        INFO: Starting pipeline
        ERROR: groovy.lang.MissingPropertyException: No such property
        WARNING: This is a warning
        """

        result = parser.parse(log_data)
        self.assertIsInstance(result, ParsedPipelineBundle)
        self.assertEqual(result.source, "jenkins")
        self.assertEqual(len(result.stages), 1)  # All in "Unknown" stage
        self.assertEqual(result.stages[0].name, "Unknown")
        self.assertGreater(len(result.stages[0].content), 0)

    def test_parse_with_stage_detection(self):
        """Test parsing with stage detection."""
        parser = PipelineParser(source="jenkins")
        log_data = """
        INFO: Starting pipeline
        [2024-01-01T12:00:00] [INFO] Stage: Build
        ERROR: groovy.lang.MissingPropertyException: No such property
        [2024-01-01T12:00:00] [INFO] Stage: Test
        WARNING: This is a warning
        """

        result = parser.parse(log_data)
        self.assertIsInstance(result, ParsedPipelineBundle)
        self.assertGreaterEqual(len(result.stages), 1)

    def test_parse_with_min_severity(self):
        """Test parsing with minimum severity filtering."""
        parser = PipelineParser(source="jenkins")
        log_data = """
        INFO: Starting pipeline
        ERROR: groovy.lang.MissingPropertyException: No such property
        WARNING: This is a warning
        CRITICAL: Critical error
        """

        # Only ERROR and CRITICAL should be included
        result = parser.parse(log_data, min_severity=SeverityLevel.ERROR)
        self.assertIsInstance(result, ParsedPipelineBundle)

        # Check that only ERROR and CRITICAL entries are included
        all_entries = []
        for stage in result.stages:
            all_entries.extend(stage.content)

        for entry in all_entries:
            self.assertIn(entry.severity, [SeverityLevel.ERROR, SeverityLevel.CRITICAL])

    def test_parse_with_deduplication(self):
        """Test parsing with deduplication enabled and disabled."""
        parser = PipelineParser(source="jenkins")
        log_data = """
        ERROR: groovy.lang.MissingPropertyException: No such property
        ERROR: groovy.lang.MissingPropertyException: No such property
        WARNING: This is a warning
        WARNING: This is a warning
        """

        # With deduplication (default)
        result_with_dedup = parser.parse(log_data, deduplicate=True)
        all_entries_dedup = []
        for stage in result_with_dedup.stages:
            all_entries_dedup.extend(stage.content)

        # Without deduplication
        result_no_dedup = parser.parse(log_data, deduplicate=False)
        all_entries_no_dedup = []
        for stage in result_no_dedup.stages:
            all_entries_no_dedup.extend(stage.content)

        self.assertGreater(len(all_entries_no_dedup), len(all_entries_dedup))

    def test_parse_with_empty_lines(self):
        """Test parsing with empty lines."""
        parser = PipelineParser(source="jenkins")
        log_data = """
        
        INFO: Starting pipeline
        
        
        ERROR: groovy.lang.MissingPropertyException: No such property
        
        """

        result = parser.parse(log_data)
        self.assertIsInstance(result, ParsedPipelineBundle)

        # Empty lines should be ignored
        all_entries = []
        for stage in result.stages:
            all_entries.extend(stage.content)

        self.assertGreater(len(all_entries), 0)

    def test_parse_invalid_input(self):
        """Test parsing with invalid input."""
        parser = PipelineParser(source="jenkins")

        # Empty string should return False from validate_input but not raise
        result = parser.parse("")  # This should work but return minimal result
        self.assertIsInstance(result, ParsedPipelineBundle)

    def test_detect_stage(self):
        """Test stage detection functionality."""
        parser = PipelineParser(source="jenkins")

        # Test with a line that should match Jenkins stage pattern
        test_line = "[2024-01-01T12:00:00] [INFO] Stage: Build"
        detected_stage = parser._detect_stage(test_line)
        self.assertIsNotNone(detected_stage)
        self.assertEqual(detected_stage, "Build")

        # Test with a line that should not match any stage pattern
        test_line_no_match = "ERROR: Some error occurred"
        detected_stage = parser._detect_stage(test_line_no_match)
        self.assertIsNone(detected_stage)

    def test_detect_stage_with_cleaner(self):
        """Test stage detection with stage name cleaning."""
        parser = PipelineParser(source="jenkins")

        # Test with a line that needs cleaning
        test_line = "[2024-01-01T12:00:00] [INFO] Stage: 1. Build"
        detected_stage = parser._detect_stage(test_line)
        self.assertIsNotNone(detected_stage)
        self.assertEqual(detected_stage, "Build")  # Should be cleaned

    def test_detect_stage_with_invalid_name(self):
        """Test stage detection with invalid stage name that gets filtered out."""
        parser = PipelineParser(source="jenkins")

        # Test with a line that matches pattern but produces invalid stage name
        test_line = "[2024-01-01T12:00:00] [INFO] Stage: user"
        detected_stage = parser._detect_stage(test_line)
        self.assertIsNone(detected_stage)  # Should be filtered out by cleaner

    def test_is_severity_enough(self):
        """Test severity level checking."""
        parser = PipelineParser(source="jenkins")

        # Test various severity combinations
        self.assertTrue(
            parser._is_severity_enough(SeverityLevel.ERROR, SeverityLevel.WARNING)
        )
        self.assertTrue(
            parser._is_severity_enough(SeverityLevel.WARNING, SeverityLevel.WARNING)
        )
        self.assertFalse(
            parser._is_severity_enough(SeverityLevel.INFO, SeverityLevel.WARNING)
        )
        self.assertTrue(
            parser._is_severity_enough(SeverityLevel.CRITICAL, SeverityLevel.ERROR)
        )
        self.assertFalse(
            parser._is_severity_enough(SeverityLevel.WARNING, SeverityLevel.ERROR)
        )

    def test_detect_language(self):
        """Test language detection functionality."""
        parser = PipelineParser(source="jenkins")

        # Test with a line that should match groovy pattern
        test_line = "ERROR: groovy.lang.MissingPropertyException: No such property"
        detected_language = parser._detect_language(test_line)
        self.assertEqual(detected_language, "groovy")

        # Test with a line that should not match any pattern
        test_line_no_match = "INFO: Starting pipeline"
        detected_language = parser._detect_language(test_line_no_match)
        self.assertIsNone(detected_language)

    def test_detect_language_with_empty_patterns(self):
        """Test language detection with empty patterns."""
        parser = PipelineParser()  # No source, so no patterns

        test_line = "ERROR: groovy.lang.MissingPropertyException: No such property"
        detected_language = parser._detect_language(test_line)
        self.assertIsNone(detected_language)

    def test_classify_severity(self):
        """Test severity classification functionality."""
        parser = PipelineParser(source="jenkins")

        # Test with a line that should match ERROR severity
        test_line = "ERROR: groovy.lang.MissingPropertyException: No such property"
        severity = parser._classify_severity("groovy", test_line)
        self.assertEqual(severity, SeverityLevel.ERROR)

        # Test with a line that should not match any pattern (defaults to INFO)
        test_line_no_match = "Some random log line"
        severity = parser._classify_severity("groovy", test_line_no_match)
        self.assertEqual(severity, SeverityLevel.INFO)

    def test_classify_severity_unknown_language(self):
        """Test severity classification with unknown language."""
        parser = PipelineParser(source="jenkins")

        # Test with unknown language
        test_line = "ERROR: Some error"
        severity = parser._classify_severity("unknown_language", test_line)
        self.assertEqual(severity, SeverityLevel.INFO)  # Should default to INFO

    def test_load_source_patterns_invalid_source(self):
        """Test loading patterns with invalid source."""
        parser = PipelineParser()

        # Test with invalid source for patterns
        with self.assertRaises(ValueError) as cm:
            parser._load_source_patterns("invalid_source")
        self.assertIn("Unknown source for patterns", str(cm.exception))

    def test_load_source_patterns_invalid_stage_source(self):
        """Test loading patterns with invalid stage source."""
        parser = PipelineParser()

        # Mock the PATTERNS to have a source that doesn't exist in STAGE_PATTERNS
        with unittest.mock.patch(
            "langops.parser.patterns.PATTERNS", {"test_source": {}}
        ):
            with unittest.mock.patch("langops.parser.patterns.STAGE_PATTERNS", {}):
                with self.assertRaises(ValueError) as context:
                    parser._load_source_patterns("test_source")

                self.assertIn(
                    "Unknown source for stage patterns: test_source",
                    str(context.exception),
                )

    def test_load_source_patterns_invalid_stage_source_only(self):
        """Test loading patterns with source that exists in PATTERNS but not in STAGE_PATTERNS."""
        parser = PipelineParser()

        # Test with a source that exists in PATTERNS but not in STAGE_PATTERNS
        with unittest.mock.patch(
            "langops.parser.patterns.PATTERNS", {"test_source": {"python": []}}
        ):
            with unittest.mock.patch("langops.parser.patterns.STAGE_PATTERNS", {}):
                with self.assertRaises(ValueError) as context:
                    parser._load_source_patterns("test_source")

                self.assertIn(
                    "Unknown source for stage patterns: test_source",
                    str(context.exception),
                )

    def test_process_line_stage_detection(self):
        """Test the _process_line method with stage detection."""
        parser = PipelineParser(source="jenkins")

        lines = ["[2024-01-01T12:00:00] [INFO] Stage: Build", "ERROR: Some error"]
        stages_map = {}
        seen_logs = set()

        # Process stage detection line
        result_stage = parser._process_line(
            "[2024-01-01T12:00:00] [INFO] Stage: Build",
            1,
            lines,
            "Unknown",
            stages_map,
            seen_logs,
            SeverityLevel.INFO,
            True,
        )

        self.assertEqual(result_stage, "Build")
        self.assertIn("Build", stages_map)
        self.assertEqual(stages_map["Build"].name, "Build")
        self.assertEqual(stages_map["Build"].start_line, 1)

    def test_process_line_log_entry(self):
        """Test the _process_line method with log entry processing."""
        parser = PipelineParser(source="jenkins")

        lines = ["INFO: Starting", "ERROR: groovy.lang.MissingPropertyException: error"]
        stages_map = {}
        seen_logs = set()

        # Process log entry line
        result_stage = parser._process_line(
            "ERROR: groovy.lang.MissingPropertyException: error",
            2,
            lines,
            "Build",
            stages_map,
            seen_logs,
            SeverityLevel.INFO,
            True,
        )

        self.assertEqual(result_stage, "Build")
        self.assertIn("Build", stages_map)
        self.assertGreater(len(stages_map["Build"].content), 0)
        self.assertEqual(stages_map["Build"].content[0].severity, SeverityLevel.ERROR)

    def test_process_line_severity_filtering(self):
        """Test the _process_line method with severity filtering."""
        parser = PipelineParser(source="jenkins")

        lines = ["INFO: Starting", "ERROR: groovy.lang.MissingPropertyException: error"]
        stages_map = {}
        seen_logs = set()

        # Process INFO line with ERROR min_severity (should be filtered out)
        result_stage = parser._process_line(
            "INFO: Starting",
            1,
            lines,
            "Build",
            stages_map,
            seen_logs,
            SeverityLevel.ERROR,
            True,
        )

        self.assertEqual(result_stage, "Build")
        # Should not create any log entry due to severity filtering
        self.assertNotIn("Build", stages_map)

    def test_process_line_deduplication(self):
        """Test the _process_line method with deduplication."""
        parser = PipelineParser(source="jenkins")

        lines = ["ERROR: groovy.lang.MissingPropertyException: error"] * 3
        stages_map = {}
        seen_logs = set()

        # Process the same line multiple times with deduplication enabled
        for i in range(3):
            parser._process_line(
                "ERROR: groovy.lang.MissingPropertyException: error",
                i + 1,
                lines,
                "Build",
                stages_map,
                seen_logs,
                SeverityLevel.INFO,
                True,
            )

        # Should only have one entry due to deduplication
        self.assertEqual(len(stages_map["Build"].content), 1)

    def test_process_line_no_deduplication(self):
        """Test the _process_line method without deduplication."""
        parser = PipelineParser(source="jenkins")

        lines = ["ERROR: groovy.lang.MissingPropertyException: error"] * 3
        stages_map = {}
        seen_logs = set()

        # Process the same line multiple times with deduplication disabled
        for i in range(3):
            parser._process_line(
                "ERROR: groovy.lang.MissingPropertyException: error",
                i + 1,
                lines,
                "Build",
                stages_map,
                seen_logs,
                SeverityLevel.INFO,
                False,
            )

        # Should have all entries without deduplication
        self.assertEqual(len(stages_map["Build"].content), 3)

    def test_process_line_stage_transition(self):
        """Test stage transition in _process_line method."""
        parser = PipelineParser(source="jenkins")

        lines = [
            "[2024-01-01T12:00:00] [INFO] Stage: Build",
            "[2024-01-01T12:00:00] [INFO] Stage: Test",
        ]
        stages_map = {
            "Build": StageWindow(name="Build", start_line=1, end_line=1, content=[])
        }
        seen_logs = set()

        # Process stage transition
        result_stage = parser._process_line(
            "[2024-01-01T12:00:00] [INFO] Stage: Test",
            2,
            lines,
            "Build",
            stages_map,
            seen_logs,
            SeverityLevel.INFO,
            True,
        )

        self.assertEqual(result_stage, "Test")
        self.assertIn("Test", stages_map)
        # Previous stage should have updated end_line
        self.assertEqual(stages_map["Build"].end_line, 1)

    def test_registry_integration(self):
        """Test that PipelineParser is properly registered."""
        # Check that the parser is registered
        self.assertIn("pipeline_parser", ParserRegistry._registry)

        # Test that we can create it through the registry
        parser = ParserRegistry.get_parser("pipeline_parser")
        self.assertIsInstance(parser, type)

    def test_parse_complete_pipeline_flow(self):
        """Test complete pipeline parsing flow with multiple stages."""
        parser = PipelineParser(source="jenkins")

        log_data = """
        INFO: Starting pipeline
        [2024-01-01T12:00:00] [INFO] Stage: Build
        ERROR: groovy.lang.MissingPropertyException: No such property
        WARNING: Build warning
        [2024-01-01T12:00:00] [INFO] Stage: Test
        ERROR: Test failed
        INFO: Test info
        [2024-01-01T12:00:00] [INFO] Stage: Deploy
        CRITICAL: Deploy failed
        """

        result = parser.parse(log_data, min_severity=SeverityLevel.INFO)

        # Should have at least some stages
        self.assertGreaterEqual(len(result.stages), 1)

        # Check that we have some content
        total_content = sum(len(stage.content) for stage in result.stages)
        self.assertGreater(total_content, 0)

    def test_parse_with_metadata_extraction(self):
        """Test parsing includes metadata extraction."""
        parser = PipelineParser(source="jenkins")

        log_data = """
        BUILD_ID=12345
        Started by user TestUser
        Branch: main
        INFO: Starting pipeline
        ERROR: groovy.lang.MissingPropertyException: No such property
        """

        result = parser.parse(log_data)

        # Should have extracted metadata
        self.assertIsNotNone(result.metadata)
        self.assertIn("build_id", result.metadata)
        self.assertEqual(result.metadata["build_id"], "12345")

    def test_parse_end_line_updates(self):
        """Test that end_line is properly updated for the last stage."""
        parser = PipelineParser(source="jenkins")

        log_data = """
        [2024-01-01T12:00:00] [INFO] Stage: Build
        ERROR: groovy.lang.MissingPropertyException: No such property
        WARNING: Build warning
        INFO: Final line
        """

        result = parser.parse(log_data)

        # Should have at least one stage
        self.assertGreater(len(result.stages), 0)

        # Find the stage (could be Build or Unknown)
        last_stage = result.stages[-1]
        self.assertGreater(last_stage.end_line, 0)

    def test_error_handling_in_parse(self):
        """Test error handling in parse method."""
        parser = PipelineParser(source="jenkins")

        # Test with malformed input that might cause issues
        log_data = "INFO: Normal line\n\x00\x01\x02Invalid characters\nERROR: groovy.lang.MissingPropertyException"

        # Should not crash, should handle gracefully
        result = parser.parse(log_data)
        self.assertIsInstance(result, ParsedPipelineBundle)


if __name__ == "__main__":
    unittest.main()
