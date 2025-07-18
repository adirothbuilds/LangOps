import re
from typing import Optional, Dict, List, Tuple, cast, Any
from langops.core.base_parser import BaseParser
from langops.parser.registry import ParserRegistry
from langops.parser.utils import PatternResolver, STAGE_NAME_CLEANERS, Extractor
from langops.parser.constants.pipeline_constants import SEVERITY_ORDER
from langops.parser.types.pipeline_types import (
    SeverityLevel,
    ParsedPipelineBundle,
    LogEntry,
    StageWindow,
)

"""
PipelineParser is a specialized parser for handling pipeline logs, such as those from Jenkins, GitHub Actions, and GitLab CI.
It can also be extended with custom patterns defined in a YAML configuration file.
"""


@ParserRegistry.register(name="pipeline_parser")
class PipelineParser(BaseParser):
    """
    Initializes the PipelineParser with predefined patterns or custom patterns from a configuration file.

    Args:
        source (Optional[str]): The source from which to load predefined patterns. Can be 'jenkins', 'github_actions', 'gitlab_ci', etc.
        config_file (Optional[str]): Path to a YAML configuration file containing custom patterns.
    """

    patterns: Dict[str, List[Tuple[re.Pattern, SeverityLevel]]]
    stage_patterns: List[re.Pattern]

    def __init__(
        self,
        source: Optional[str] = None,
        config_file: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        self.source = source or "unknown"
        self.patterns = {}
        self.stage_patterns = []
        self.additional_kwargs = kwargs

        if source:
            self.patterns, self.stage_patterns = self._load_source_patterns(source)

        if config_file:
            custom_patterns = PatternResolver.load_patterns(config_file)
            self.source = custom_patterns.get("source", self.source)
            self.patterns.update(custom_patterns.get("patterns", {}))
            self.stage_patterns.extend(custom_patterns.get("stage_patterns", []))

    def parse(
        self,
        data: str,
        min_severity: SeverityLevel = SeverityLevel.WARNING,
        deduplicate: bool = True,
    ) -> ParsedPipelineBundle:
        """
        Parses the given pipeline log data into a structured format.

        Args:
            data (str): The raw log data to parse.
            min_severity (SeverityLevel): The minimum severity level to include in the parsed output.
            deduplicate (bool): Whether to deduplicate log entries based on their content.

        Returns:
            ParsedPipelineBundle: A structured representation of the parsed pipeline logs.
        """
        self.validate_input(data)

        current_stage = "Unknown"
        stages_map: Dict[str, StageWindow] = {}
        seen_logs: set[str] = set()
        lines = data.splitlines()

        for line_number, line in enumerate(lines, start=1):
            line = line.strip()
            if not line:
                continue

            current_stage = self._process_line(
                line,
                line_number,
                lines,
                current_stage,
                stages_map,
                seen_logs,
                min_severity,
                deduplicate,
            )

        if current_stage in stages_map:
            stages_map[current_stage].end_line = max(
                stages_map[current_stage].end_line, line_number
            )

        return ParsedPipelineBundle(
            source=self.source,
            stages=list(stages_map.values()),
            metadata=Extractor.metadata(data),
        )

    def _process_line(
        self,
        line: str,
        line_number: int,
        lines: List[str],
        current_stage: str,
        stages_map: Dict[str, StageWindow],
        seen_logs: set[str],
        min_severity: SeverityLevel,
        deduplicate: bool,
    ) -> str:
        """
        Processes a single line of log data to extract relevant information and update the current stage.

        Args:
            line (str): The log line to process.
            line_number (int): The current line number in the log data.
            lines (List[str]): The complete list of log lines.
            current_stage (str): The name of the current stage being processed.
            stages_map (Dict[str, StageWindow]): A map of stage names to their corresponding StageWindow objects.
            seen_logs (set[str]): A set of already seen log entries to avoid duplicates.
            min_severity (SeverityLevel): The minimum severity level to include in the parsed output.
            deduplicate (bool): Whether to deduplicate log entries based on their content.

        Returns:
            str: The updated current stage name after processing the line.
        """
        detected_stage = self._detect_stage(line)
        if detected_stage:
            if current_stage in stages_map:
                stages_map[current_stage].end_line = line_number - 1

            if detected_stage not in stages_map:
                stages_map[detected_stage] = StageWindow(
                    name=detected_stage,
                    start_line=line_number,
                    end_line=line_number,
                    content=[],
                )
            return detected_stage

        language = self._detect_language(line) or "unknown"
        severity = self._classify_severity(language, line)
        if not self._is_severity_enough(severity, min_severity):
            return current_stage

        if deduplicate and line in seen_logs:
            return current_stage
        seen_logs.add(line)

        log_entry = LogEntry(
            timestamp=Extractor.timestamp(line),
            language=language,
            severity=severity,
            line=line_number,
            message=line,
            context_id=Extractor.context_id(
                lines, line_number, self.additional_kwargs.get("window_size", 20)
            ),
        )

        if current_stage not in stages_map:
            stages_map[current_stage] = StageWindow(
                name=current_stage,
                start_line=line_number,
                end_line=line_number,
                content=[],
            )
        stages_map[current_stage].content.append(log_entry)

        return current_stage

    def _load_source_patterns(self, source: str) -> Tuple[Dict, List]:
        """
        Loads predefined patterns and stage patterns based on the specified source.

        Args:
            source (str): The source from which to load patterns. Can be 'jenkins', 'github_actions', 'gitlab_ci', etc.

        Returns:
            Tuple[Dict, List]: A tuple containing two elements:
                - A dictionary of compiled regex patterns for different languages.
                - A list of compiled regex patterns for stages.

        Raises:
            ValueError: If the source is not recognized or does not have associated patterns.
        """
        from langops.parser.patterns import PATTERNS, STAGE_PATTERNS

        if source in PATTERNS:
            patterns = PatternResolver.resolve_patterns(
                cast(Dict[str, Any], PATTERNS[source])
            )
        else:
            raise ValueError(f"Unknown source for patterns: {source}")

        if source in STAGE_PATTERNS:
            stage_patterns = STAGE_PATTERNS[source]
        else:
            raise ValueError(f"Unknown source for stage patterns: {source}")

        return patterns, stage_patterns

    def _detect_stage(self, line: str) -> Optional[str]:
        """
        Detects the stage name from a log line using multiple regex patterns.

        Args:
            line (str): The log line to analyze.

        Returns:
            Optional[str]: The detected stage name, or None if no stage is detected.
        """
        for pattern in self.stage_patterns:
            match = pattern.match(line)
            if match:
                cleaner = STAGE_NAME_CLEANERS.get(
                    self.source, STAGE_NAME_CLEANERS["default"]
                )
                cleaned_stage_name = cleaner(match.group(1))
                if cleaned_stage_name:
                    return cleaned_stage_name
        return None

    def _is_severity_enough(
        self, current_severity: SeverityLevel, min_severity: SeverityLevel
    ) -> bool:
        """
        Checks if the severity of a log line is above the minimum severity level.

        Args:
            line (str): The log line to analyze.
            min_severity (SeverityLevel): The minimum severity level to check against.

        Returns:
            bool: True if the line's severity is above or equal to the minimum severity, False otherwise.
        """
        return SEVERITY_ORDER.index(current_severity) >= SEVERITY_ORDER.index(
            min_severity
        )

    def _detect_language(self, line: str) -> Optional[str]:
        """
        Detects the programming language of a log line based on predefined patterns.

        Args:
            line (str): The log line to analyze.

        Returns:
            Optional[str]: The detected programming language, or None if not recognized.
        """
        for language, patterns in self.patterns.items():
            for pattern, _ in patterns:
                if pattern.search(line):
                    return language
        return None

    def _classify_severity(self, language: str, line: str) -> SeverityLevel:
        """
        Classifies the severity of a log line based on predefined patterns.

        Args:
            line (str): The log line to classify.

        Returns:
            SeverityLevel: The classified severity level.
        """
        for pattern, level in self.patterns.get(language, []):
            if pattern.search(line):
                return level
        return SeverityLevel.INFO
