from enum import Enum
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class SeverityLevel(str, Enum):
    """
    Enum representing the severity levels for pipeline patterns.
    Each level corresponds to a specific type of issue that can be detected in pipeline logs.
    """

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class LogEntry(BaseModel):
    """
    Represents a single log entry in a pipeline log.

    Attributes:
        timestamp (Optional[datetime]): The timestamp of the log entry.
        language (Optional[str]): The programming language associated with the log entry.
        severity (SeverityLevel): The severity level of the log entry.
        line (int): The line number in the source code where the log entry originated.
        message (str): The message content of the log entry.
        context_id (Optional[str]): An optional identifier for additional context, such as a stage or job ID.
    """

    timestamp: Optional[datetime]
    language: Optional[str] = None
    severity: SeverityLevel
    line: int
    message: str
    context_id: Optional[str] = None

    def dict(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """
        Override the Pydantic dict method to ensure JSON serialization compatibility.
        """
        return {
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "language": self.language,
            "severity": self.severity.value,
            "line": self.line,
            "message": self.message,
            "context_id": self.context_id,
        }


class StageWindow(BaseModel):
    """
    Represents a stage in a pipeline, containing logs and metadata.

    Attributes:
        name (str): The name of the stage.
        start_line (int): The starting line number of the stage in the source code.
        end_line (int): The ending line number of the stage in the source code.
        content (List[LogEntry]): A list of log entries associated with this stage.
    """

    name: str
    start_line: int
    end_line: int
    content: List[LogEntry]

    def dict(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """
        Override the Pydantic dict method to ensure JSON serialization compatibility.
        """
        return {
            "name": self.name,
            "start_line": self.start_line,
            "end_line": self.end_line,
            "content": [log.dict() for log in self.content],
        }


class ParsedPipelineBundle(BaseModel):
    """
    Represents a parsed bundle of pipeline logs, including metadata and stages.

    Attributes:
        source (str): The source of the pipeline logs (e.g., 'jenkins', 'github_actions').
        stages (List[StageWindow]): A list of stages in the pipeline, each containing logs and metadata.
        metadata (Optional[Dict[str, Any]]): Additional metadata about the pipeline run, such as duration, status, etc.
    """

    source: str
    stages: List[StageWindow]
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """
        Custom to_dict method to ensure compatibility with BaseParser.to_dict.
        """
        return self.dict()
