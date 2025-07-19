from langops.parser.types.pipeline_types import (
    SeverityLevel,
    ParsedPipelineBundle,
    LogEntry,
    StageWindow,
)

PIPELINE_TYPES = {
    "SeverityLevel": SeverityLevel,
    "ParsedPipelineBundle": ParsedPipelineBundle,
    "LogEntry": LogEntry,
    "StageWindow": StageWindow,
}

__all__ = ["PIPELINE_TYPES"]
