import pytest
from langops.parser.types.pipeline_types import (
    SeverityLevel,
    LogEntry,
    StageWindow,
    ParsedPipelineBundle,
)


def test_severity_level_enum():
    """Test the SeverityLevel enum values."""
    assert SeverityLevel.INFO.value == "info"
    assert SeverityLevel.WARNING.value == "warning"
    assert SeverityLevel.ERROR.value == "error"
    assert SeverityLevel.CRITICAL.value == "critical"


def test_log_entry_dict():
    """Test the dict method of LogEntry."""
    entry = LogEntry(
        timestamp=None,
        language="python",
        severity=SeverityLevel.INFO,
        line=42,
        message="This is a log message.",
        context_id="12345",
    )
    expected_dict = {
        "timestamp": None,
        "language": "python",
        "severity": "info",
        "line": 42,
        "message": "This is a log message.",
        "context_id": "12345",
    }
    assert entry.dict() == expected_dict


def test_stage_window_dict():
    """Test the dict method of StageWindow."""
    entry = LogEntry(
        timestamp=None,
        language="python",
        severity=SeverityLevel.INFO,
        line=42,
        message="This is a log message.",
        context_id="12345",
    )
    stage = StageWindow(name="Build Stage", start_line=1, end_line=100, content=[entry])
    expected_dict = {
        "name": "Build Stage",
        "start_line": 1,
        "end_line": 100,
        "content": [entry.dict()],
    }
    assert stage.dict() == expected_dict


def test_parsed_pipeline_bundle_model_dump():
    """Test the model_dump method of ParsedPipelineBundle."""
    entry = LogEntry(
        timestamp=None,
        language="python",
        severity=SeverityLevel.INFO,
        line=42,
        message="This is a log message.",
        context_id="12345",
    )
    stage = StageWindow(name="Build Stage", start_line=1, end_line=100, content=[entry])
    bundle = ParsedPipelineBundle(stages=[stage], source="jenkins", metadata=None)
    expected_dict = {
        "stages": [stage.model_dump()],
        "source": "jenkins",
        "metadata": None,
    }
    assert bundle.model_dump() == expected_dict
