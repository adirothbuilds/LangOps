# JenkinsParser

## Overview

`JenkinsParser` filters Jenkins logs by severity level. It extracts stage, severity, and timestamp information to reduce noise before further analysis or LLM processing.

## API Documentation

### Methods

#### `parse(data)`

**Description**: Parse Jenkins logs and return structured data.

**Arguments**:

- `data` (str): The log file content as a string.

**Returns**:

- [`ParsedLogBundle`](../core/types.md#parsedlogbundle): Structured representation of parsed logs.

#### `filter_by_severity(data, severity)`

**Description**: Filters Jenkins logs by a specific severity level.

**Arguments**:

- `data` (str): The log file content as a string.
- `severity` (str): Severity level to filter logs (e.g., "ERROR", "WARNING").

**Returns**:

- `list`: List of log lines matching the specified severity.

#### `extract_stage_info(data)`

**Description**: Extracts stage information from Jenkins logs using regex patterns.

**Arguments**:

- `data` (str): The log file content as a string.

**Returns**:

- `dict`: Dictionary containing stage names and their corresponding log lines.

---

## Usage

To use `JenkinsParser`, instantiate it and call the `parse` method with Jenkins log data.

```python
from langops.parser.jenkins_parser import JenkinsParser

parser = JenkinsParser()
parsed_logs = parser.parse("jenkins log content here")
print(parsed_logs)

# Example: Filter logs by severity
error_logs = parser.filter_by_severity("jenkins log content here", "ERROR")
print(error_logs)

# Example: Extract stage information
stage_info = parser.extract_stage_info("jenkins log content here")
print(stage_info)
```

---

## Integration

`JenkinsParser` works seamlessly with other modules like `ErrorParser` and `ParserRegistry`. For example, you can register `JenkinsParser` using `ParserRegistry` and use it in a pipeline with `ErrorParser` for comprehensive log analysis.
