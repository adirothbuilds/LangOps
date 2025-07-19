# Pipeline Types

## Overview

The `pipeline_types.py` module defines the core data structures and types used throughout the LangOps pipeline parsing system. These types provide a consistent interface for representing log entries, pipeline stages, and parsed results.

## Enums

### `SeverityLevel`

An enumeration representing the severity levels for pipeline patterns and log entries.

```python
class SeverityLevel(str, Enum):
    """
    Enum representing the severity levels for pipeline patterns.
    Each level corresponds to a specific type of issue that can be detected in pipeline logs.
    """
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
```

**Values:**

- `INFO`: Informational messages that don't indicate problems
- `WARNING`: Warnings that don't stop execution but may indicate issues
- `ERROR`: Errors that may cause failure or unexpected behavior
- `CRITICAL`: Critical errors that typically stop execution

**Example:**

```python
from langops.parser.types.pipeline_types import SeverityLevel

# Use in pattern definitions
severity = SeverityLevel.ERROR
print(severity.value)  # "error"

# Compare severity levels
if severity == SeverityLevel.ERROR:
    print("This is an error")

# Get all severity levels
all_levels = list(SeverityLevel)
print(all_levels)  # [SeverityLevel.INFO, SeverityLevel.WARNING, ...]
```

## Data Models

### `LogEntry`

Represents a single log entry in a pipeline log with structured metadata.

```python
class LogEntry(BaseModel):
    """
    Represents a single log entry in a pipeline log.
    """
    timestamp: Optional[datetime]
    language: Optional[str] = None
    severity: SeverityLevel
    line: int
    message: str
    context_id: Optional[str] = None
```

**Attributes:**

- `timestamp` (Optional[datetime]): The timestamp of the log entry
- `language` (Optional[str]): The programming language associated with the log entry
- `severity` (SeverityLevel): The severity level of the log entry
- `line` (int): The line number in the source code where the log entry originated
- `message` (str): The message content of the log entry
- `context_id` (Optional[str]): An optional identifier for additional context

**Methods:**

- `dict()`: Returns a dictionary representation with JSON-serializable values

**Example:**

```python
from langops.parser.types.pipeline_types import LogEntry, SeverityLevel
from datetime import datetime

# Create a log entry
log_entry = LogEntry(
    timestamp=datetime.now(),
    language="python",
    severity=SeverityLevel.ERROR,
    line=42,
    message="Traceback (most recent call last):",
    context_id="build-123"
)

# Convert to dictionary
log_dict = log_entry.dict()
print(log_dict)
# {
#     'timestamp': '2024-01-01T12:00:00',
#     'language': 'python',
#     'severity': 'error',
#     'line': 42,
#     'message': 'Traceback (most recent call last):',
#     'context_id': 'build-123'
# }
```

### `StageWindow`

Represents a stage in a pipeline, containing logs and metadata for a specific execution phase.

```python
class StageWindow(BaseModel):
    """
    Represents a stage in a pipeline, containing logs and metadata.
    """
    name: str
    start_line: int
    end_line: int
    content: List[LogEntry]
```

**Attributes:**

- `name` (str): The name of the stage
- `start_line` (int): The starting line number of the stage in the source code
- `end_line` (int): The ending line number of the stage in the source code
- `content` (List[LogEntry]): A list of log entries associated with this stage

**Methods:**

- `dict()`: Returns a dictionary representation with JSON-serializable values

**Example:**

```python
from langops.parser.types.pipeline_types import StageWindow, LogEntry, SeverityLevel

# Create log entries for the stage
log_entries = [
    LogEntry(
        timestamp=None,
        language="python",
        severity=SeverityLevel.INFO,
        line=1,
        message="Starting build process",
        context_id=None
    ),
    LogEntry(
        timestamp=None,
        language="python",
        severity=SeverityLevel.ERROR,
        line=10,
        message="Build failed",
        context_id=None
    )
]

# Create a stage window
stage = StageWindow(
    name="Build",
    start_line=1,
    end_line=20,
    content=log_entries
)

# Convert to dictionary
stage_dict = stage.dict()
print(stage_dict["name"])  # "Build"
print(len(stage_dict["content"]))  # 2
```

### `ParsedPipelineBundle`

Represents a complete parsed bundle of pipeline logs, including metadata and stages.

```python
class ParsedPipelineBundle(BaseModel):
    """
    Represents a parsed bundle of pipeline logs, including metadata and stages.
    """
    source: str
    stages: List[StageWindow]
    metadata: Optional[Dict[str, Any]] = None
```

**Attributes:**

- `source` (str): The source of the pipeline logs (e.g., 'jenkins', 'github_actions')
- `stages` (List[StageWindow]): A list of stages in the pipeline
- `metadata` (Optional[Dict[str, Any]]): Additional metadata about the pipeline run

**Methods:**

- `to_dict()`: Custom method for compatibility with BaseParser.to_dict
- `dict()`: Standard Pydantic dictionary conversion

**Example:**

```python
from langops.parser.types.pipeline_types import ParsedPipelineBundle, StageWindow, LogEntry, SeverityLevel

# Create stages
stages = [
    StageWindow(
        name="Build",
        start_line=1,
        end_line=50,
        content=[
            LogEntry(
                timestamp=None,
                language="python",
                severity=SeverityLevel.INFO,
                line=1,
                message="Starting build",
                context_id=None
            )
        ]
    ),
    StageWindow(
        name="Test",
        start_line=51,
        end_line=100,
        content=[
            LogEntry(
                timestamp=None,
                language="python",
                severity=SeverityLevel.ERROR,
                line=75,
                message="Test failed",
                context_id=None
            )
        ]
    )
]

# Create pipeline bundle
bundle = ParsedPipelineBundle(
    source="jenkins",
    stages=stages,
    metadata={
        "build_id": "build-123",
        "duration": 120,
        "status": "failed"
    }
)

# Convert to dictionary
bundle_dict = bundle.to_dict()
print(bundle_dict["source"])  # "jenkins"
print(len(bundle_dict["stages"]))  # 2
print(bundle_dict["metadata"]["build_id"])  # "build-123"
```

## Usage Patterns

### Creating Log Entries

```python
from langops.parser.types.pipeline_types import LogEntry, SeverityLevel
from datetime import datetime

def create_log_entry(message: str, line: int, severity: str = "info") -> LogEntry:
    """Helper function to create log entries."""
    return LogEntry(
        timestamp=datetime.now(),
        language=None,
        severity=SeverityLevel(severity),
        line=line,
        message=message,
        context_id=None
    )

# Create log entries
info_log = create_log_entry("Build started", 1, "info")
error_log = create_log_entry("Build failed", 10, "error")
```

### Processing Pipeline Results

```python
from langops.parser.types.pipeline_types import ParsedPipelineBundle, SeverityLevel

def analyze_pipeline_results(bundle: ParsedPipelineBundle) -> Dict[str, int]:
    """Analyze pipeline results and return severity counts."""
    severity_counts = {level.value: 0 for level in SeverityLevel}
    
    for stage in bundle.stages:
        for log_entry in stage.content:
            severity_counts[log_entry.severity.value] += 1
    
    return severity_counts

# Use with parsed results
bundle = ParsedPipelineBundle(...)
analysis = analyze_pipeline_results(bundle)
print(analysis)  # {'info': 5, 'warning': 2, 'error': 1, 'critical': 0}
```

### Stage Analysis

```python
from langops.parser.types.pipeline_types import StageWindow, SeverityLevel

def find_failed_stages(bundle: ParsedPipelineBundle) -> List[str]:
    """Find stages that contain critical or error messages."""
    failed_stages = []
    
    for stage in bundle.stages:
        has_failure = any(
            log.severity in [SeverityLevel.ERROR, SeverityLevel.CRITICAL]
            for log in stage.content
        )
        if has_failure:
            failed_stages.append(stage.name)
    
    return failed_stages

# Find failed stages
failed_stages = find_failed_stages(bundle)
print(failed_stages)  # ['Build', 'Test']
```

## Serialization

### JSON Serialization

All types are designed to be JSON-serializable:

```python
import json
from langops.parser.types.pipeline_types import LogEntry, SeverityLevel
from datetime import datetime

# Create a log entry
log_entry = LogEntry(
    timestamp=datetime.now(),
    language="python",
    severity=SeverityLevel.ERROR,
    line=42,
    message="Error occurred",
    context_id="ctx-123"
)

# Serialize to JSON
json_str = json.dumps(log_entry.dict())
print(json_str)

# Deserialize from JSON
data = json.loads(json_str)
reconstructed = LogEntry(**data)
```

### Custom Serialization

```python
from langops.parser.types.pipeline_types import ParsedPipelineBundle

def serialize_bundle(bundle: ParsedPipelineBundle) -> Dict[str, Any]:
    """Custom serialization for pipeline bundles."""
    return {
        "source": bundle.source,
        "stage_count": len(bundle.stages),
        "total_logs": sum(len(stage.content) for stage in bundle.stages),
        "metadata": bundle.metadata or {}
    }

# Use custom serialization
summary = serialize_bundle(bundle)
print(summary)
```

## Integration with Parsers

### Parser Return Types

```python
from langops.parser.types.pipeline_types import ParsedPipelineBundle
from langops.parser.base_parser import BaseParser

class CustomParser(BaseParser):
    def parse(self, data: str) -> ParsedPipelineBundle:
        """Parse pipeline logs and return structured results."""
        # Parse the data
        stages = self._parse_stages(data)
        metadata = self._extract_metadata(data)
        
        return ParsedPipelineBundle(
            source=self.source,
            stages=stages,
            metadata=metadata
        )
```

### Type Checking

```python
from langops.parser.types.pipeline_types import LogEntry, SeverityLevel
from typing import List

def validate_log_entries(entries: List[LogEntry]) -> bool:
    """Validate a list of log entries."""
    for entry in entries:
        if not isinstance(entry, LogEntry):
            return False
        if not isinstance(entry.severity, SeverityLevel):
            return False
        if entry.line < 0:
            return False
    return True
```

## Performance Considerations

- **Pydantic Models**: Use Pydantic for validation and serialization
- **Memory Usage**: Large pipeline bundles may consume significant memory
- **Serialization**: Use `dict()` methods for efficient serialization
- **Type Validation**: Pydantic provides automatic type validation

## Best Practices

### Model Usage

1. **Validation**: Always use Pydantic validation for data integrity
2. **Serialization**: Use built-in `dict()` methods for consistent serialization
3. **Type Hints**: Use proper type hints for better IDE support
4. **Documentation**: Document model fields and their purposes

### Error Handling

```python
from langops.parser.types.pipeline_types import LogEntry, SeverityLevel
from pydantic import ValidationError

def safe_create_log_entry(data: Dict[str, Any]) -> Optional[LogEntry]:
    """Safely create a log entry with validation."""
    try:
        return LogEntry(**data)
    except ValidationError as e:
        print(f"Validation error: {e}")
        return None
```

## Testing

The pipeline types module is thoroughly tested with:

- **Model Validation**: Tests for Pydantic model validation
- **Serialization**: Tests for JSON serialization and deserialization
- **Type Safety**: Tests for type checking and validation
- **Edge Cases**: Tests for boundary conditions and invalid data
