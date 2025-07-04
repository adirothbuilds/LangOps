import re
from datetime import datetime
from typing import Optional
from langops.core.base_parser import BaseParser
from langops.core.constants import SEVERITY_ORDER
from langops.core.types import SeverityLevel
from langops.core.types import ParsedLogBundle
from langops.core.types import LogEntry
from langops.core.types import StageLogs
from langops.parser.registry import ParserRegistry
from langops.parser import jenkins_patterns


@ParserRegistry.register(name="JenkinsParser")
class JenkinsParser(BaseParser):
    """
    Parser that filters Jenkins logs by severity level.
    Extracts stage, severity, and timestamp info to reduce noise
    before further analysis or LLM processing.

    Supports multiple Jenkins pipeline stage detection patterns and
    provides comprehensive log analysis with deduplication capabilities.
    """

    def __init__(self):
        self.patterns = (
            jenkins_patterns.GROOVY_PATTERNS
            + jenkins_patterns.JAVA_PATTERNS
            + jenkins_patterns.NODEJS_PATTERNS
            + jenkins_patterns.PYTHON_PATTERNS
            + jenkins_patterns.DOTNET_PATTERNS
            + jenkins_patterns.SH_PATTERNS
            + jenkins_patterns.SONAR_PATTERNS
            + jenkins_patterns.JFROG_PATTERNS
            + jenkins_patterns.DOCKER_PATTERNS
            + jenkins_patterns.JENKINS_PATTERNS
            + jenkins_patterns.HTTP_PATTERNS
            + jenkins_patterns.TEST_PATTERNS
            + jenkins_patterns.LINT_PATTERNS
        )

        # Enhanced stage detection patterns for different Jenkins pipeline formats
        self.stage_patterns = jenkins_patterns.STAGE_PATTERNS

    def parse(
        self,
        data: str,
        min_severity: SeverityLevel = SeverityLevel.WARNING,
        deduplicate: bool = True,
    ) -> ParsedLogBundle:
        """
        Parse Jenkins log data, filtering by severity level and deduplicating entries.

        Args:
            data (str): The Jenkins log data to parse.
            min_severity (SeverityLevel): Minimum severity level to include in results.
            deduplicate (bool): Whether to deduplicate log entries.

        Returns:
            ParsedLogBundle: Parsed log entries with metadata.

        Raises:
            ValueError: If input data is invalid.
        """
        self.validate_input(data)
        current_stage = "Unknown"
        stage_map: dict[str, list[LogEntry]] = {}
        seen_messages: set[str] = set()

        for line in data.splitlines():
            line = line.strip()
            if not line:  # Skip empty lines
                continue

            # Detect stage name using multiple patterns
            detected_stage = self._detect_stage(line)
            if detected_stage:
                current_stage = detected_stage
                continue

            severity = self._classify_severity(line)
            if not self._is_severity_enough(severity, min_severity):
                continue

            # Use original line for deduplication to avoid losing context
            if deduplicate and line in seen_messages:
                continue

            seen_messages.add(line)

            if current_stage not in stage_map:
                stage_map[current_stage] = []

            stage_map[current_stage].append(
                LogEntry(
                    timestamp=self._extract_timestamp(line),
                    message=line,
                    severity=severity,
                )
            )

        return ParsedLogBundle(
            stages=[
                StageLogs(name=stage, logs=entries)
                for stage, entries in stage_map.items()
                if entries  # Only include stages with actual log entries
            ]
        )

    def _detect_stage(self, line: str) -> Optional[str]:
        """
        Detect Jenkins pipeline stage name from a log line using multiple patterns.

        Args:
            line (str): The log line to analyze.

        Returns:
            Optional[str]: The detected stage name or None if not found.
        """
        for pattern in self.stage_patterns:
            match = pattern.search(line)
            if match:
                stage_name = match.group(1).strip()

                # Skip invalid or unwanted stage names
                if (
                    not stage_name
                    or len(stage_name) < 2
                    or stage_name.lower() in {"user", "admin", "system", "sh"}
                ):
                    continue

                # Clean up common Jenkins artifacts from stage names
                stage_name = re.sub(
                    r"^\d+[\.\)]\s*", "", stage_name
                )  # Remove numbering
                stage_name = re.sub(
                    r"\s*\[.*?\]$", "", stage_name
                )  # Remove trailing bracketed annotations from stage names

                # Handle Pipeline stages differently
                if stage_name.lower() == "pipeline":
                    # For [Pipeline] sh, return "Pipeline"
                    return "Pipeline"

                return stage_name
        return None

    def _classify_severity(self, line: str) -> SeverityLevel:
        """
        Classify the severity of a log line based on predefined patterns.

        Args:
            line (str): The log line to classify.

        Returns:
            SeverityLevel: The classified severity level.
        """
        for pattern, level in self.patterns:
            if pattern.search(line):
                return level
        return SeverityLevel.INFO

    def _is_severity_enough(
        self, level: SeverityLevel, min_level: SeverityLevel
    ) -> bool:
        """
        Check if the severity level is greater than or equal to the minimum level.

        Args:
            level (SeverityLevel): The severity level of the log entry.
            min_level (SeverityLevel): The minimum severity level to include.

        Returns:
            bool: True if the log entry's severity is sufficient, False otherwise.
        """
        return SEVERITY_ORDER.index(level) >= SEVERITY_ORDER.index(min_level)

    def _extract_timestamp(self, line: str) -> Optional[datetime]:
        """
        Extract the timestamp from a log line if present.

        Supports multiple timestamp formats commonly found in Jenkins logs.

        Args:
            line (str): The log line to extract the timestamp from.

        Returns:
            Optional[datetime]: The extracted timestamp or None if not found.
        """
        # Multiple timestamp patterns for different Jenkins log formats
        timestamp_patterns = [
            r"(\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}(?:[,\.]\d{3})?)",  # ISO format
            r"(\w{3}\s+\d{1,2}\s+\d{4}\s+\d{2}:\d{2}:\d{2})",  # Mon DD YYYY HH:MM:SS
            r"(\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2}:\d{2})",  # MM/DD/YYYY HH:MM:SS
        ]

        for pattern in timestamp_patterns:
            match = re.search(pattern, line)
            if match:
                try:
                    timestamp_str = match.group(1)
                    # Normalize timestamp format
                    timestamp_str = timestamp_str.replace(" ", "T").replace(",", ".")
                    return datetime.fromisoformat(timestamp_str)
                except ValueError:
                    continue
        return None

    def get_stages_summary(
        self, parsed_data: ParsedLogBundle
    ) -> dict[str, dict[str, int]]:
        """
        Get a summary of stages with count of log entries by severity level.

        Args:
            parsed_data (ParsedLogBundle): The parsed log data.

        Returns:
            dict[str, dict[str, int]]: Summary with stage names and severity counts.
        """
        summary: dict[str, dict[str, int]] = {}
        for stage in parsed_data.stages:
            severity_counts: dict[str, int] = {}
            for entry in stage.logs:
                severity = entry.severity.value
                severity_counts[severity] = severity_counts.get(severity, 0) + 1
            summary[stage.name] = severity_counts
        return summary
