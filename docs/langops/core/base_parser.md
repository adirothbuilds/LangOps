# BaseParser

## Overview

`BaseParser` is an abstract base class for all parsers. It provides utility methods for file handling, filtering, validation, and serialization.

## API Documentation

### Methods

#### `parse(data)`

**Description**: Parse the input data and return the result.

**Arguments**:

- `data` (Any): The data to be parsed.

**Returns**:

- `Any`: The parsed result.

---

#### `handle_log_file(log_file_path)`

**Description**: Reads and returns the content of the log file.

**Arguments**:

- `log_file_path` (str): Path to the log file.

**Returns**:

- `str`: Content of the log file.

---

#### `filter_log_lines(log_content, keyword=None, level=None, pattern=None, flags=0)`

**Description**: Filter log lines by keyword, log level, or regex pattern.

**Arguments**:

- `log_content` (str): The content of the log file.
- `keyword` (str, optional): Keyword to filter lines.
- `level` (str, optional): Log level to filter lines.
- `pattern` (str, optional): Regex pattern to filter lines.
- `flags` (int, optional): Regex flags.

**Returns**:

- `list`: Filtered log lines.

---

#### `validate_input(data)`

**Description**: Validate input data. Override for custom validation in subclasses.

**Arguments**:

- `data` (Any): Input data to validate.

**Raises**:

- `ValueError`: If data is None or not a string.

**Returns**:

- `bool`: True if valid.

---

#### `from_file(file_path, *args, **kwargs)`

**Description**: Parse data directly from a file path. Must be called from a concrete subclass.

**Arguments**:

- `file_path` (str): Path to the file.
- `*args`: Arguments for subclass constructor.
- `**kwargs`: Keyword arguments for subclass constructor.

**Raises**:

- `NotImplementedError`: If called on BaseParser directly.

**Returns**:

- `Any`: Parsed result from the file.

---

#### `to_dict(parsed_result)`

**Description**: Convert parsed result to a dictionary if possible.

**Arguments**:

- `parsed_result` (Any): The result to convert.

**Raises**:

- `TypeError`: If conversion is not possible.

**Returns**:

- `dict`: Dictionary representation of the parsed result.

---

#### `to_json(parsed_result)`

**Description**: Convert parsed result to a JSON string.

**Arguments**:

- `parsed_result` (Any): The result to convert.

**Raises**:

- `NotImplementedError`: If called on BaseParser directly.
- `ValueError`: If conversion to JSON fails.

**Returns**:

- `str`: JSON string representation of the parsed result.

---

## Usage

To implement a custom parser, inherit from `BaseParser` and override the required methods.

```python
from langops.core.base_parser import BaseParser

class CustomParser(BaseParser):
    def parse(self, data):
        return json.loads(data)
```
