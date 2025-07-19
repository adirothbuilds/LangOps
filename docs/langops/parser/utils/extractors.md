# Extractors

## Overview

The `extractors.py` module provides utilities for extracting meaningful information from log entries, including timestamps, context IDs, and metadata. These functions are essential for parsing and structuring unstructured log data.

## Functions

### `extract_timestamp(line: str) -> Optional[datetime]`

Extracts a timestamp from a given line of text and returns it as a datetime object.

**Parameters:**

- `line` (str): The line of text to search for a timestamp

**Returns:**

- `Optional[datetime]`: The extracted timestamp as a datetime object, or None if no timestamp is found

**Supported Formats:**

- ISO 8601: `2024-01-01T12:00:00`, `2024-01-01 12:00:00`
- Common log formats: `01/Jan/2024:12:00:00`
- Time-only format: `12:00:00`
- Custom formats: `2024/01/01 12:00:00`

**Example:**

```python
from langops.parser.utils.extractors import extract_timestamp

# Extract from ISO format
timestamp = extract_timestamp("2024-01-01T12:00:00Z [INFO] Starting build")
print(timestamp)  # 2024-01-01 12:00:00

# Extract from log format
timestamp = extract_timestamp("01/Jan/2024:12:00:00 [ERROR] Build failed")
print(timestamp)  # 2024-01-01 12:00:00

# No timestamp found
timestamp = extract_timestamp("Build completed successfully")
print(timestamp)  # None
```

### `extract_context_id(lines: List[str], line_number: int, window: int = 20) -> Optional[str]`

Extracts a context ID from a list of log lines around a specific line number.

**Parameters:**

- `lines` (List[str]): The list of log lines
- `line_number` (int): The line number to extract context from
- `window` (int, optional): The number of lines before and after to consider (default: 20)

**Returns:**

- `Optional[str]`: The extracted context ID or None if not found

**Context ID Patterns:**

- Hexadecimal IDs: `a1b2c3d4-e5f6-7890`
- Context IDs: `context-id: abc123`
- Trace IDs: `trace-id: xyz789`
- Job IDs: `job-id: build-456`
- Build IDs: `build-id: 123`
- Exception patterns: `Exception: SomeError`

**Example:**

```python
from langops.parser.utils.extractors import extract_context_id

log_lines = [
    "Starting build process",
    "context-id: abc123def456",
    "ERROR: Build failed",
    "Cleaning up resources"
]

context_id = extract_context_id(log_lines, line_number=2)
print(context_id)  # "abc123def456"
```

### `extract_metadata(data: str, source: Optional[str] = None) -> Dict[str, Any]`

Extracts metadata from the pipeline log data.

**Parameters:**

- `data` (str): The raw log data from which to extract metadata
- `source` (Optional[str]): The source of the pipeline logs (e.g., 'jenkins', 'github_actions')

**Returns:**

- `Dict[str, Any]`: A dictionary containing extracted metadata

**Extracted Metadata:**

- `build_id`: Build identifier
- `triggered_by`: User who triggered the build
- `branch`: Git branch name
- `pipeline_system`: The CI/CD system used
- `start_time`: Build start timestamp

**Example:**

```python
from langops.parser.utils.extractors import extract_metadata

log_data = """
BUILD_ID=build-123
Started by user john.doe
Branch: main
[2024-01-01T12:00:00Z] Starting pipeline
"""

metadata = extract_metadata(log_data, source="jenkins")
print(metadata)
# {
#     'build_id': 'build-123',
#     'triggered_by': 'john.doe',
#     'branch': 'main',
#     'pipeline_system': 'jenkins',
#     'start_time': datetime(2024, 1, 1, 12, 0, 0)
# }
```

## Internal Functions

### `_match_patterns(line: str) -> Optional[str]`

Matches a line against predefined patterns to extract context ID. This is an internal function used by `extract_context_id`.

### `_collect_context_lines(lines: List[str], start: int, end: int, keywords: List[str]) -> List[str]`

Collects context lines that contain specific keywords. This is an internal function used by `extract_context_id`.

## Usage Patterns

### Combining Extractors

```python
from langops.parser.utils.extractors import extract_timestamp, extract_context_id, extract_metadata

def process_log_entry(lines: List[str], line_number: int, full_log: str) -> Dict[str, Any]:
    """Process a single log entry and extract all available information."""
    line = lines[line_number]
    
    return {
        'timestamp': extract_timestamp(line),
        'context_id': extract_context_id(lines, line_number),
        'metadata': extract_metadata(full_log, source="jenkins")
    }
```

### Error Handling

```python
from langops.parser.utils.extractors import extract_timestamp
from datetime import datetime

def safe_extract_timestamp(line: str) -> datetime:
    """Extract timestamp with fallback to current time."""
    timestamp = extract_timestamp(line)
    return timestamp if timestamp else datetime.now()
```

## Performance Considerations

- **Regex Optimization**: All patterns are compiled with appropriate flags for performance
- **Window Size**: The context window size affects performance; adjust based on your needs
- **Pattern Matching**: Patterns are ordered by frequency for optimal matching speed
- **Memory Usage**: Large log files should be processed in chunks to avoid memory issues

## Extensibility

### Adding New Timestamp Formats

To add support for new timestamp formats, extend the `timestamp_patterns` list in `extract_timestamp`:

```python
# Add new pattern to timestamp_patterns
new_pattern = (
    r"\b\d{4}-\d{3} \d{2}:\d{2}:\d{2}\b",  # YYYY-DDD HH:MM:SS
    ["%Y-%j %H:%M:%S"]
)
```

### Adding New Context ID Patterns

To add support for new context ID patterns, extend the `context_id_patterns` list in `_match_patterns`:

```python
# Add new pattern to context_id_patterns
new_pattern = re.compile(r"\bcustom[-_]?id[:=\s]?([a-zA-Z0-9-]{6,})\b", re.IGNORECASE)
```

## Testing

The extractors module is thoroughly tested with 100% code coverage:

- **Timestamp Extraction**: Tests for all supported formats and edge cases
- **Context ID Extraction**: Tests for pattern matching and context window logic
- **Metadata Extraction**: Tests for various log formats and missing data scenarios
- **Error Handling**: Tests for invalid inputs and edge cases
