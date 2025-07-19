import unittest
from datetime import datetime
from langops.parser.types.pipeline_types import (
    SeverityLevel,
    LogEntry,
    StageWindow,
    ParsedPipelineBundle,
)


class TestPipelineTypes(unittest.TestCase):

    def test_severity_level_enum(self):
        self.assertEqual(SeverityLevel.INFO.value, "info")
        self.assertEqual(SeverityLevel.WARNING.value, "warning")
        self.assertEqual(SeverityLevel.ERROR.value, "error")
        self.assertEqual(SeverityLevel.CRITICAL.value, "critical")

    def test_log_entry(self):
        timestamp = datetime.now()
        log_entry = LogEntry(
            timestamp=timestamp,
            language="Python",
            severity=SeverityLevel.ERROR,
            line=42,
            message="An error occurred",
            context_id="stage-1",
        )

        self.assertEqual(log_entry.timestamp, timestamp)
        self.assertEqual(log_entry.language, "Python")
        self.assertEqual(log_entry.severity, SeverityLevel.ERROR)
        self.assertEqual(log_entry.line, 42)
        self.assertEqual(log_entry.message, "An error occurred")
        self.assertEqual(log_entry.context_id, "stage-1")
        self.assertEqual(
            log_entry.dict(),
            {
                "timestamp": timestamp.isoformat(),
                "language": "Python",
                "severity": "error",
                "line": 42,
                "message": "An error occurred",
                "context_id": "stage-1",
            },
        )

    def test_stage_window(self):
        log_entry = LogEntry(
            timestamp=None,
            language="Python",
            severity=SeverityLevel.WARNING,
            line=10,
            message="A warning",
            context_id=None,
        )
        stage_window = StageWindow(
            name="Build Stage", start_line=1, end_line=20, content=[log_entry]
        )

        self.assertEqual(stage_window.name, "Build Stage")
        self.assertEqual(stage_window.start_line, 1)
        self.assertEqual(stage_window.end_line, 20)
        self.assertEqual(len(stage_window.content), 1)
        self.assertEqual(stage_window.content[0], log_entry)
        self.assertEqual(
            stage_window.dict(),
            {
                "name": "Build Stage",
                "start_line": 1,
                "end_line": 20,
                "content": [log_entry.dict()],
            },
        )

    def test_parsed_pipeline_bundle(self):
        stage_window = StageWindow(
            name="Test Stage", start_line=1, end_line=10, content=[]
        )
        parsed_bundle = ParsedPipelineBundle(
            source="jenkins",
            stages=[stage_window],
            metadata={"duration": "5m", "status": "success"},
        )

        self.assertEqual(parsed_bundle.source, "jenkins")
        self.assertEqual(len(parsed_bundle.stages), 1)
        self.assertEqual(parsed_bundle.stages[0], stage_window)
        self.assertEqual(
            parsed_bundle.metadata, {"duration": "5m", "status": "success"}
        )
        self.assertEqual(
            parsed_bundle.to_dict(),
            {
                "source": "jenkins",
                "stages": [stage_window.dict()],
                "metadata": {"duration": "5m", "status": "success"},
            },
        )


if __name__ == "__main__":
    unittest.main()
