# ErrorParser Documentation

## Overview

`ErrorParser` is a parser class that extracts error log lines from log file content. It is registered in the parser registry and extends `BaseParser`, leveraging its flexible filtering utilities.

### Inherits

- `BaseParser`

### Registration

- Registered automatically with `@ParserRegistry.register()`.

### Methods

#### parse(self, data)

Parses the input log content and returns only error log lines.

**Args:**

- `data` (str): The log file content as a string.

**Returns:**

- `list`: List of error log lines (matching 'err', 'error', 'ERR', 'ERROR', etc., case-insensitive).

#### to_dict(cls, parsed_result)

Converts the list of error log lines to a dictionary.

**Args:**

- `parsed_result` (list): List of error log lines.

**Returns:**

- `dict`: Dictionary with error log lines under the 'errors' key.

#### to_json(cls, parsed_result)

Converts the error log lines to a JSON string.

**Args:**

- `parsed_result` (list): List of error log lines.

**Returns:**

- `str`: JSON string representation of the error log lines.

## Example Usage

```python
from langops.parser import ErrorParser

log_content = """
2025-06-21 10:00:00 INFO Starting process
2025-06-21 10:01:00 ERROR Failed to connect
2025-06-21 10:02:00 err Disk full
2025-06-21 10:03:00 WARNING Low memory
"""

parser = ErrorParser()
error_lines = parser.parse(log_content)
print(error_lines)  # ['2025-06-21 10:01:00 ERROR Failed to connect', '2025-06-21 10:02:00 err Disk full']
print(ErrorParser.to_json(error_lines))
```

## Notes

- Uses a regex pattern to match any common error keyword (case-insensitive).
- Leverages the improved `filter_log_lines` from `BaseParser` for robust filtering.
- Can be extended for more advanced error log extraction if needed.
