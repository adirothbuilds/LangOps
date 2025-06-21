# BaseParser Documentation

## Overview

`BaseParser` is an abstract base class designed to provide a robust foundation for building custom parser classes in Python. It includes essential parsing interfaces and utility methods for file handling, log filtering, input validation, and serialization. Several methods are class methods to allow easy overriding for custom logic in subclasses.

## Class: BaseParser

### Abstract Methods

- `parse(self, data)`
  - Abstract method to be implemented by subclasses.
  - Parses the input data and returns the result.
  - Args:
    - `data` (Any): The data to be parsed.
  - Returns: The parsed result.

### Static Methods

- `handle_log_file(log_file_path)`
  - Reads and returns the content of a log file.
  - Args:
    - `log_file_path` (str): Path to the log file.
  - Returns: Content of the log file as a string.

- `filter_log_lines(log_content, keyword=None, level=None, pattern=None, flags=0)`
  - Filters log lines by a keyword, log level, or regex pattern.
  - Args:
    - `log_content` (str): The content of the log file.
    - `keyword` (str, optional): Keyword to filter lines.
    - `level` (str, optional): Log level to filter lines (e.g., 'ERROR', 'INFO').
    - `pattern` (str, optional): Regex pattern to filter lines.
    - `flags` (int, optional): Regex flags (e.g., re.IGNORECASE).
  - Returns: List of filtered log lines.

### Class Methods

- `validate_input(cls, data)`
  - Validates input data. Override for custom validation in subclasses.
  - Args:
    - `data` (Any): Input data to validate.
  - Raises: `ValueError` if data is None.
  - Returns: `True` if valid.

- `from_file(cls, file_path, *args, **kwargs)`
  - Parses data directly from a file path. Must be called from a concrete subclass.
  - Args:
    - `file_path` (str): Path to the file.
    - `*args, **kwargs`: Arguments for subclass constructor.
  - Returns: Parsed result from the file.
  - Raises: `NotImplementedError` if called on `BaseParser` directly.
  - Note: Uses `handle_log_file` to read file content before parsing.

- `to_dict(cls, parsed_result)`
  - Converts a parsed result to a dictionary if possible. Override for custom serialization in subclasses.
  - Args:
    - `parsed_result` (Any): The result to convert.
  - Returns: Dictionary representation.
  - Raises: `TypeError` if conversion is not possible.
  - Note: Supports objects with `to_dict`, `__dict__`, or is already a `dict`.

- `to_json(cls, parsed_result)`
  - Converts a parsed result to a JSON string. Override for custom serialization in subclasses.
  - Args:
    - `parsed_result` (Any): The result to convert.
  - Returns: JSON string.
  - Raises: `NotImplementedError` if called on `BaseParser` directly, or `ValueError` if conversion fails.
  - Note: Uses `to_dict` for conversion and outputs pretty-printed JSON.

## Usage Example

```python
class MyParser(BaseParser):
    def parse(self, data):
        # Implement custom parsing logic
        return data.upper()

result = MyParser.from_file('example.txt')
print(result)
```

## Notes

- Always subclass `BaseParser` and implement the `parse` method.
- Use provided static and class methods for common parsing utilities.
- Override class methods like `validate_input`, `to_dict`, and `to_json` for custom logic as needed.
- `filter_log_lines` now supports regex-based filtering for advanced use cases.
- `to_dict` also supports objects with a `__dict__` attribute.
- `to_json` outputs indented, sorted, and UTF-8 safe JSON.
