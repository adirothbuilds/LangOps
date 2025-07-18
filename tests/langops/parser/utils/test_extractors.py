import unittest
from datetime import datetime
from langops.parser.utils.extractors import (
    extract_timestamp,
    extract_context_id,
    extract_metadata,
)


class TestExtractors(unittest.TestCase):

    def test_extract_timestamp(self):
        line_with_timestamp = "2025-07-18 12:34:56,789 INFO Starting process"
        line_without_timestamp = "INFO Starting process"

        timestamp = extract_timestamp(line_with_timestamp)
        self.assertIsInstance(timestamp, datetime)
        self.assertEqual(timestamp.year, 2025)
        self.assertEqual(timestamp.month, 7)
        self.assertEqual(timestamp.day, 18)
        self.assertEqual(timestamp.hour, 12)
        self.assertEqual(timestamp.minute, 34)
        self.assertEqual(timestamp.second, 56)

        self.assertIsNone(extract_timestamp(line_without_timestamp))

    def test_extract_context_id(self):
        lines = [
            "INFO Starting process",
            "context_id=abc123",
            "ERROR Something went wrong",
            "trace_id=xyz789",
            "FAIL src/main.py",
            "Exception: ValueError",
        ]

        context_id = extract_context_id(lines, line_number=1)
        self.assertEqual(context_id, "abc123")

        trace_id = extract_context_id(lines, line_number=3)
        self.assertEqual(trace_id, "xyz789")

        fail_context = extract_context_id(lines, line_number=4)
        self.assertEqual(fail_context, "src/main.py")

        exception_context = extract_context_id(lines, line_number=5)
        self.assertEqual(exception_context, "ValueError")

        # Line 0 should find context from nearby lines within the window
        context_from_window = extract_context_id(lines, line_number=0)
        self.assertEqual(context_from_window, "abc123")

    def test_extract_metadata(self):
        log_data = """
        BUILD_ID=12345
        Started by user JohnDoe
        Branch: main
        2025-07-18 12:34:56,789 INFO Starting process
        """

        metadata = extract_metadata(log_data, source="jenkins_pipeline")
        self.assertEqual(metadata["build_id"], "12345")
        self.assertEqual(metadata["triggered_by"], "JohnDoe")
        self.assertEqual(metadata["branch"], "main")
        self.assertEqual(metadata["pipeline_system"], "jenkins_pipeline")
        self.assertIsInstance(metadata["start_time"], datetime)

    def test_extract_timestamp_edge_cases(self):
        # Test time-only format that defaults to year 1900 (lines 39-40)
        time_only_line = "12:34:56 INFO Starting process"
        timestamp = extract_timestamp(time_only_line)
        self.assertIsInstance(timestamp, datetime)
        self.assertEqual(timestamp.hour, 12)
        self.assertEqual(timestamp.minute, 34)
        self.assertEqual(timestamp.second, 56)
        # Should be current year/month/day since original was 1900
        now = datetime.now()
        self.assertEqual(timestamp.year, now.year)
        self.assertEqual(timestamp.month, now.month)
        self.assertEqual(timestamp.day, now.day)

        # Test invalid format that causes ValueError (lines 44-45)
        invalid_format_line = "2025-13-45 25:67:89 INFO Invalid timestamp"
        timestamp = extract_timestamp(invalid_format_line)
        self.assertIsNone(timestamp)

    def test_extract_context_id_edge_cases(self):
        # Test case where context lines are found and joined (lines 79-83)
        lines = [
            "INFO Starting process",
            "Some error occurred",
            "Failed to connect",
            "Exception happened",
            "DEBUG Details",
        ]

        # Should find pattern matches first, not context lines
        context_id = extract_context_id(lines, line_number=2, window=5)
        self.assertIsInstance(context_id, str)
        # The function finds "occurred" from the Error pattern match
        self.assertEqual(context_id, "occurred")

    def test_extract_context_id_no_matches(self):
        # Test case where no pattern matches are found but context lines exist
        lines = [
            "INFO Starting process",
            "failed operation",
            "error in system",
            "trace information",
        ]

        context_id = extract_context_id(lines, line_number=1, window=3)
        # Should return joined context lines since no pattern matches
        self.assertIsInstance(context_id, str)
        self.assertIn(" | ", context_id)

    def test_collect_context_lines_with_date_filter(self):
        # Test the regex filter that excludes lines starting with date patterns (line 134)
        from langops.parser.utils.extractors import _collect_context_lines

        lines = [
            "[2025-07-18 12:34:56] Error occurred",  # Should be filtered out
            "2025-07-18 Regular error message",  # Should be included
            "ERROR: Something failed",  # Should be included
            "[2025-07-18] Another timestamped error",  # Should be filtered out
            "FAIL: Test failed",  # Should be included
        ]

        keywords = ["error", "fail"]
        context_lines = _collect_context_lines(lines, 0, len(lines), keywords)

        # Should include lines with keywords but exclude those starting with [YYYY-MM-DD
        self.assertEqual(len(context_lines), 3)
        self.assertIn("2025-07-18 Regular error message", context_lines)
        self.assertIn("ERROR: Something failed", context_lines)
        self.assertIn("FAIL: Test failed", context_lines)

        # Should not include lines starting with [YYYY-MM-DD
        for line in context_lines:
            self.assertFalse(line.startswith("[2025-"))

    def test_extract_context_id_empty_lines(self):
        # Test with empty lines list
        context_id = extract_context_id([], line_number=0)
        self.assertIsNone(context_id)

    def test_extract_context_id_out_of_bounds(self):
        # Test with line number out of bounds
        lines = ["INFO Starting process", "ERROR Something failed"]
        context_id = extract_context_id(lines, line_number=10, window=5)
        # When line number is way out of bounds, window may be empty
        self.assertIsNone(context_id)

        # Test with line number slightly out of bounds but still in window
        lines = ["INFO Starting process", "ERROR Something failed", "Another line"]
        context_id = extract_context_id(lines, line_number=3, window=5)
        # Should find "Something" from the ERROR pattern match within window
        self.assertEqual(context_id, "Something")

    def test_match_patterns_edge_cases(self):
        from langops.parser.utils.extractors import _match_patterns

        # Test patterns that should be filtered out (too short, common words, etc.)
        self.assertIsNone(_match_patterns("Error: ab"))  # Too short
        self.assertIsNone(_match_patterns("Error: the"))  # Common word pattern
        self.assertIsNone(_match_patterns("Error: 'quoted'"))  # Contains quotes
        self.assertIsNone(
            _match_patterns("Error: (parentheses)")
        )  # Contains parentheses

        # Test valid patterns
        self.assertEqual(_match_patterns("Error: SomeValidError"), "SomeValidError")
        self.assertEqual(_match_patterns("trace_id=abc123def"), "abc123def")
        self.assertEqual(
            _match_patterns("job_id=build-12345"), "build-12345"
        )  # Use underscore, not hyphen

    def test_extract_metadata_edge_cases(self):
        # Test metadata extraction with missing fields
        log_data_minimal = "Some log without metadata"
        metadata = extract_metadata(log_data_minimal)
        self.assertEqual(metadata, {})

        # Test with source that doesn't contain "pipeline"
        log_data = """
        BUILD_ID=12345
        Started by user JohnDoe
        Branch: main
        """
        metadata = extract_metadata(log_data, source="jenkins")
        self.assertEqual(metadata["build_id"], "12345")
        self.assertEqual(metadata["triggered_by"], "JohnDoe")
        self.assertEqual(metadata["branch"], "main")
        self.assertNotIn("pipeline_system", metadata)

        # Test with no timestamp
        log_data_no_timestamp = """
        BUILD_ID=54321
        Started by user JaneDoe
        """
        metadata = extract_metadata(
            log_data_no_timestamp, source="github_actions_pipeline"
        )
        self.assertEqual(metadata["build_id"], "54321")
        self.assertEqual(metadata["triggered_by"], "JaneDoe")
        self.assertEqual(metadata["pipeline_system"], "github_actions_pipeline")
        self.assertNotIn("start_time", metadata)


if __name__ == "__main__":
    unittest.main()
