import re
import yaml
from typing import Dict, List, Any
from langops.parser.patterns.common import COMMON_PATTERNS
from langops.parser.types.pipeline_types import SeverityLevel


class PatternResolver:
    """
    A helper class for resolving and loading patterns for different platforms and languages.
    """

    @staticmethod
    def resolve_patterns(platform_dict: Dict[str, Any]) -> Dict[str, List]:
        """
        Resolves patterns for different languages based on the provided platform dictionary.

        Args:
            platform_dict (Dict[str, Any]):
                A dictionary where keys are language names and values are either:
                - A list of tuples (regex, severity).
                - A string indicating a common pattern (e.g., "common.python").

        Returns:
            Dict[str, List]:
                A dictionary with resolved patterns for each language. If a common pattern is referenced,
                it is replaced with the corresponding patterns from the COMMON_PATTERNS dictionary.

        Raises:
            KeyError: If a referenced common pattern key is missing.
            Exception: For any unexpected errors during resolution.
        """
        resolved_patterns = {}
        for language, patterns in platform_dict.items():
            if isinstance(patterns, str) and patterns.startswith("common."):
                language_key = patterns.split(".")[1]
                if language_key not in COMMON_PATTERNS:
                    raise KeyError(f"Missing key in COMMON_PATTERNS: '{language_key}'")
                resolved_patterns[language] = COMMON_PATTERNS[language_key]
            else:
                resolved_patterns[language] = patterns
        return resolved_patterns

    @staticmethod
    def load_patterns(config_file: str) -> Dict[str, Any]:
        """
        Loads custom patterns from a YAML configuration file.

        Args:
            config_file (str):
                Path to the YAML configuration file containing custom patterns.

        Returns:
            Dict[str, Any]:
                A dictionary with two keys:
                - 'patterns': A dictionary where keys are languages and values are lists of tuples (regex, severity).
                - 'stage_patterns': A list of compiled regex patterns for stage detection.

        Raises:
            FileNotFoundError: If the configuration file is not found.
            yaml.YAMLError: If there is an error parsing the YAML file.
            KeyError: If the YAML structure is missing required keys.
            Exception: For any unexpected errors during loading.
        """
        with open(config_file, "r") as file:
            try:
                raw_data = yaml.safe_load(file)
            except yaml.YAMLError as e:
                raise yaml.YAMLError(f"Error parsing YAML file: {e}")

        if not isinstance(raw_data, dict):
            raise KeyError("Top-level structure in YAML must be a dictionary")

        source = raw_data.get("source")
        raw_patterns = raw_data.get("patterns", {})
        raw_stage_patterns = raw_data.get("stage_patterns", [])

        if not isinstance(raw_patterns, dict):
            raise KeyError("'patterns' section must be a dictionary")

        patterns = {}
        for lang, pattern_list in raw_patterns.items():
            if not isinstance(pattern_list, list):
                raise KeyError(f"Expected list of patterns for language '{lang}'")
            patterns[lang] = [
                (re.compile(p["regex"], re.IGNORECASE), SeverityLevel[p["severity"]])
                for p in pattern_list
                if "regex" in p and "severity" in p
            ]

        stage_patterns = [
            re.compile(p, re.IGNORECASE)
            for p in raw_stage_patterns
            if isinstance(p, str)
        ]

        return {
            "source": source,
            "patterns": patterns,
            "stage_patterns": stage_patterns,
        }
