# PipelineParser

## Overview

The `PipelineParser` class is a specialized parser for handling pipeline logs from various CI/CD platforms such as Jenkins, GitHub Actions, and GitLab CI. It provides intelligent stage detection, severity classification, and metadata extraction.

## Class Definition

```python
@ParserRegistry.register(name="pipeline_parser")
class PipelineParser(BaseParser):
    """
    Advanced parser for CI/CD pipeline logs with intelligent stage detection.
    """
```

## Features

- **Multi-platform Support**: Jenkins, GitHub Actions, GitLab CI, and more
- **Intelligent Stage Detection**: Automatic pipeline stage identification and cleaning
- **Severity Classification**: Context-aware error severity assessment
- **Metadata Extraction**: Timestamps, build IDs, and contextual information
- **Configurable Filtering**: Minimum severity levels and deduplication
- **Pattern-based Matching**: Extensible pattern system for different platforms

## Constructor

```python
def __init__(self, source: Optional[str] = None, config_file: Optional[str] = None, **kwargs):
```

**Parameters:**

- `source` (str, optional): The source platform to load predefined patterns from. Supported values: `"jenkins"`, `"github_actions"`, `"gitlab_ci"`, `"azure_devops"`
- `config_file` (str, optional): Path to a YAML configuration file containing custom patterns
- `**kwargs`: Additional configuration options

**Example:**

```python
from langops.parser import PipelineParser

# Initialize with Jenkins patterns
parser = PipelineParser(source="jenkins")

# Initialize with custom configuration
parser = PipelineParser(config_file="custom_patterns.yaml")

# Initialize with both
parser = PipelineParser(source="jenkins", config_file="additional_patterns.yaml")
```

## Methods

### `parse(data, min_severity=None, deduplicate=False, extract_metadata=True)`

Parse pipeline log data and return structured results.

**Parameters:**

- `data` (str or List[str]): Log data to parse (string or list of log lines)
- `min_severity` (SeverityLevel, optional): Minimum severity level to include in results
- `deduplicate` (bool, default=False): Whether to remove duplicate log entries
- `extract_metadata` (bool, default=True): Whether to extract metadata from log lines

**Returns:**

- `ParsedPipelineBundle`: Structured result containing log entries, stages, and metadata

**Example:**

```python
from langops.parser.types import SeverityLevel

# Basic parsing
result = parser.parse(log_content)

# Advanced parsing with filtering
result = parser.parse(
    log_content,
    min_severity=SeverityLevel.WARNING,
    deduplicate=True,
    extract_metadata=True
)

# Access results
print(f"Found {len(result.log_entries)} log entries")
print(f"Stages: {[stage.name for stage in result.stages]}")
print(f"Summary: {result.summary}")
```

### `_detect_stage(line: str) -> Optional[str]`

Detect pipeline stage from a log line.

**Parameters:**

- `line` (str): Log line to analyze

**Returns:**

- `Optional[str]`: Stage name if detected, None otherwise

### `_classify_severity(line: str, language: str) -> SeverityLevel`

Classify the severity level of a log line.

**Parameters:**

- `line` (str): Log line to classify
- `language` (str): Programming language context

**Returns:**

- `SeverityLevel`: Classified severity level

### `_detect_language(line: str) -> str`

Detect the programming language context from a log line.

**Parameters:**

- `line` (str): Log line to analyze

**Returns:**

- `str`: Detected language or "unknown"

## Configuration

### YAML Configuration Format

```yaml
source: custom_pipeline
patterns:
  python:
    - regex: "Error:"
      severity: "ERROR"
    - regex: "Warning:"
      severity: "WARNING"
  java:
    - regex: "Exception:"
      severity: "ERROR"
stage_patterns:
  - "##\\\\[section\\\\]Starting: (.+)"
  - "##\\\\[section\\\\]Finishing: (.+)"
```

### Supported Platforms

| Platform | Source Value | Description |
|----------|--------------|-------------|
| Jenkins | `"jenkins"` | Jenkins pipeline and freestyle jobs |
| GitHub Actions | `"github_actions"` | GitHub Actions workflows |
| GitLab CI | `"gitlab_ci"` | GitLab CI/CD pipelines |
| Azure DevOps | `"azure_devops"` | Azure DevOps pipelines |

## Usage Examples

### Basic Usage

```python
from langops.parser import PipelineParser

# Create parser for Jenkins
parser = PipelineParser(source="jenkins")

# Parse log file
with open("build.log", "r") as f:
    log_content = f.read()

result = parser.parse(log_content)

# Process results
for entry in result.log_entries:
    print(f"[{entry.severity}] {entry.message}")
```

### Advanced Usage with Filtering

```python
from langops.parser import PipelineParser
from langops.parser.types import SeverityLevel

# Create parser with custom configuration
parser = PipelineParser(
    source="github_actions",
    config_file="custom_patterns.yaml"
)

# Parse with advanced options
result = parser.parse(
    log_content,
    min_severity=SeverityLevel.WARNING,
    deduplicate=True,
    extract_metadata=True
)

# Access structured data
print(f"Build Status: {result.summary.get('status', 'unknown')}")
print(f"Total Errors: {len([e for e in result.log_entries if e.severity == SeverityLevel.ERROR])}")
print(f"Stages: {len(result.stages)}")

# Process by stage
for stage in result.stages:
    stage_errors = [e for e in result.log_entries if e.stage == stage.name]
    print(f"Stage '{stage.name}': {len(stage_errors)} errors")
```

### Custom Pattern Integration

```python
# Load custom patterns from file
parser = PipelineParser(config_file="my_patterns.yaml")

# Or combine with existing patterns
parser = PipelineParser(
    source="jenkins",
    config_file="additional_patterns.yaml"
)
```

## Error Handling

The parser includes comprehensive error handling:

```python
try:
    result = parser.parse(log_content)
except ValueError as e:
    print(f"Parsing error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Performance Considerations

- **Large Log Files**: Parser handles large log files efficiently
- **Memory Usage**: Streaming processing for memory efficiency
- **Pattern Matching**: Optimized regex compilation and caching
- **Deduplication**: Optional deduplication for reducing result size

---

## See Also

- [ParsedPipelineBundle](types/pipeline_types.md): Result data structure
- [SeverityLevel](types/pipeline_types.md): Severity level enumeration
- [Pattern Configuration](patterns/index.md): Pattern configuration guide
- [Parser Registry](registry.md): Parser registration system
