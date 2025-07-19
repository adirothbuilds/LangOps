import unittest
import tempfile
import os
import yaml
from langops.parser.utils.resolver import PatternResolver
from langops.parser.types.pipeline_types import SeverityLevel


class TestPatternResolver(unittest.TestCase):

    def test_resolve_patterns_basic(self):
        """Test basic pattern resolution with regular patterns."""
        platform_dict = {
            "python": [
                ("error pattern", SeverityLevel.ERROR),
                ("warning pattern", SeverityLevel.WARNING),
            ],
            "nodejs": [
                ("js error", SeverityLevel.ERROR),
            ],
        }

        resolved = PatternResolver.resolve_patterns(platform_dict)

        self.assertEqual(resolved["python"], platform_dict["python"])
        self.assertEqual(resolved["nodejs"], platform_dict["nodejs"])

    def test_resolve_patterns_with_common_reference(self):
        """Test pattern resolution with common pattern references."""
        platform_dict = {
            "python": "common.python",
            "nodejs": "common.nodejs",
            "custom": [("custom pattern", SeverityLevel.INFO)],
        }

        resolved = PatternResolver.resolve_patterns(platform_dict)

        # Should resolve common patterns from COMMON_PATTERNS
        self.assertIn("python", resolved)
        self.assertIn("nodejs", resolved)
        self.assertIn("custom", resolved)

        # Common patterns should be replaced with actual patterns
        self.assertIsInstance(resolved["python"], list)
        self.assertIsInstance(resolved["nodejs"], list)
        self.assertEqual(resolved["custom"], platform_dict["custom"])

    def test_resolve_patterns_missing_common_key(self):
        """Test pattern resolution with missing common pattern key."""
        platform_dict = {
            "python": "common.nonexistent",
        }

        with self.assertRaises(KeyError) as cm:
            PatternResolver.resolve_patterns(platform_dict)

        self.assertIn(
            "Missing key in COMMON_PATTERNS: 'nonexistent'", str(cm.exception)
        )

    def test_resolve_patterns_empty_dict(self):
        """Test pattern resolution with empty dictionary."""
        platform_dict = {}

        resolved = PatternResolver.resolve_patterns(platform_dict)

        self.assertEqual(resolved, {})

    def test_resolve_patterns_mixed_types(self):
        """Test pattern resolution with mixed pattern types."""
        platform_dict = {
            "python": "common.python",
            "nodejs": [("custom js pattern", SeverityLevel.ERROR)],
            "java": "common.java",
        }

        resolved = PatternResolver.resolve_patterns(platform_dict)

        self.assertIn("python", resolved)
        self.assertIn("nodejs", resolved)
        self.assertIn("java", resolved)

        # Check that common patterns are resolved
        self.assertIsInstance(resolved["python"], list)
        self.assertIsInstance(resolved["java"], list)
        # Custom patterns should remain as-is
        self.assertEqual(resolved["nodejs"], platform_dict["nodejs"])

    def test_load_patterns_valid_yaml(self):
        """Test loading patterns from valid YAML file."""
        yaml_content = """
source: test_pipeline
patterns:
  python:
    - regex: "Error:"
      severity: "ERROR"
    - regex: "Warning:"
      severity: "WARNING"
  nodejs:
    - regex: "TypeError:"
      severity: "ERROR"
stage_patterns:
  - "##\\\\[section\\\\]Starting: (.+)"
  - "##\\\\[section\\\\]Finishing: (.+)"
"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(yaml_content)
            f.flush()

            try:
                result = PatternResolver.load_patterns(f.name)

                self.assertEqual(result["source"], "test_pipeline")
                self.assertIn("patterns", result)
                self.assertIn("stage_patterns", result)

                # Check patterns structure
                self.assertIn("python", result["patterns"])
                self.assertIn("nodejs", result["patterns"])

                # Check that patterns are compiled and have correct severity
                python_patterns = result["patterns"]["python"]
                self.assertEqual(len(python_patterns), 2)

                # Check first pattern
                _, severity = python_patterns[0]
                self.assertEqual(severity, SeverityLevel.ERROR)

                # Check stage patterns are compiled
                stage_patterns = result["stage_patterns"]
                self.assertEqual(len(stage_patterns), 2)

            finally:
                os.unlink(f.name)

    def test_load_patterns_file_not_found(self):
        """Test loading patterns from non-existent file."""
        with self.assertRaises(FileNotFoundError):
            PatternResolver.load_patterns("/nonexistent/file.yaml")

    def test_load_patterns_invalid_yaml(self):
        """Test loading patterns from invalid YAML file."""
        invalid_yaml = """
source: test
patterns:
  python:
    - regex: "Error:"
      severity: "ERROR"
    - invalid_yaml_syntax: [unclosed_bracket
"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(invalid_yaml)
            f.flush()

            try:
                with self.assertRaises(yaml.YAMLError):
                    PatternResolver.load_patterns(f.name)
            finally:
                os.unlink(f.name)

    def test_load_patterns_non_dict_top_level(self):
        """Test loading patterns with non-dictionary top-level structure."""
        yaml_content = """
- item1
- item2
"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(yaml_content)
            f.flush()

            try:
                with self.assertRaises(KeyError) as cm:
                    PatternResolver.load_patterns(f.name)

                self.assertIn(
                    "Top-level structure in YAML must be a dictionary",
                    str(cm.exception),
                )
            finally:
                os.unlink(f.name)

    def test_load_patterns_invalid_patterns_structure(self):
        """Test loading patterns with invalid patterns structure."""
        yaml_content = """
source: test
patterns: "not_a_dict"
"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(yaml_content)
            f.flush()

            try:
                with self.assertRaises(KeyError) as cm:
                    PatternResolver.load_patterns(f.name)

                self.assertIn(
                    "'patterns' section must be a dictionary", str(cm.exception)
                )
            finally:
                os.unlink(f.name)

    def test_load_patterns_invalid_language_patterns(self):
        """Test loading patterns with invalid language pattern structure."""
        yaml_content = """
source: test
patterns:
  python: "not_a_list"
"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(yaml_content)
            f.flush()

            try:
                with self.assertRaises(KeyError) as cm:
                    PatternResolver.load_patterns(f.name)

                self.assertIn(
                    "Expected list of patterns for language 'python'", str(cm.exception)
                )
            finally:
                os.unlink(f.name)

    def test_load_patterns_missing_pattern_fields(self):
        """Test loading patterns with missing regex or severity fields."""
        yaml_content = """
source: test
patterns:
  python:
    - regex: "Error:"
      # Missing severity
    - severity: "ERROR"
      # Missing regex
    - regex: "Warning:"
      severity: "WARNING"
"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(yaml_content)
            f.flush()

            try:
                result = PatternResolver.load_patterns(f.name)

                # Should only include patterns with both regex and severity
                python_patterns = result["patterns"]["python"]
                self.assertEqual(len(python_patterns), 1)  # Only the complete pattern

                _, severity = python_patterns[0]
                self.assertEqual(severity, SeverityLevel.WARNING)

            finally:
                os.unlink(f.name)

    def test_load_patterns_invalid_stage_patterns(self):
        """Test loading patterns with invalid stage pattern types."""
        yaml_content = """
source: test
patterns:
  python:
    - regex: "Error:"
      severity: "ERROR"
stage_patterns:
  - "##\\\\[section\\\\]Starting: (.+)"
  - 123  # Invalid type - should be string
  - "##\\\\[section\\\\]Finishing: (.+)"
"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(yaml_content)
            f.flush()

            try:
                result = PatternResolver.load_patterns(f.name)

                # Should only include string stage patterns
                stage_patterns = result["stage_patterns"]
                self.assertEqual(len(stage_patterns), 2)  # Only the string patterns

            finally:
                os.unlink(f.name)

    def test_load_patterns_minimal_yaml(self):
        """Test loading patterns from minimal YAML file."""
        yaml_content = """
source: minimal_test
"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(yaml_content)
            f.flush()

            try:
                result = PatternResolver.load_patterns(f.name)

                self.assertEqual(result["source"], "minimal_test")
                self.assertEqual(result["patterns"], {})
                self.assertEqual(result["stage_patterns"], [])

            finally:
                os.unlink(f.name)

    def test_load_patterns_no_source(self):
        """Test loading patterns without source field."""
        yaml_content = """
patterns:
  python:
    - regex: "Error:"
      severity: "ERROR"
"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(yaml_content)
            f.flush()

            try:
                result = PatternResolver.load_patterns(f.name)

                self.assertIsNone(result["source"])
                self.assertIn("patterns", result)

            finally:
                os.unlink(f.name)

    def test_load_patterns_empty_yaml(self):
        """Test loading patterns from empty YAML file."""
        yaml_content = ""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(yaml_content)
            f.flush()

            try:
                with self.assertRaises(KeyError):
                    PatternResolver.load_patterns(f.name)

            finally:
                os.unlink(f.name)

    def test_load_patterns_with_compiled_patterns(self):
        """Test that loaded patterns are properly compiled."""
        yaml_content = """
source: test
patterns:
  python:
    - regex: "(?i)error"
      severity: "ERROR"
stage_patterns:
  - "(?i)starting"
"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(yaml_content)
            f.flush()

            try:
                result = PatternResolver.load_patterns(f.name)

                # Check that patterns are compiled regex objects
                python_patterns = result["patterns"]["python"]
                pattern, _ = python_patterns[0]
                self.assertTrue(hasattr(pattern, "search"))  # Compiled regex method

                # Check stage patterns are compiled
                stage_pattern = result["stage_patterns"][0]
                self.assertTrue(
                    hasattr(stage_pattern, "search")
                )  # Compiled regex method

            finally:
                os.unlink(f.name)


if __name__ == "__main__":
    unittest.main()
