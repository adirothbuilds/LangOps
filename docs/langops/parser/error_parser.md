# ErrorParser

## Overview

`ErrorParser` filters and returns only error logs from the input data.

## API Documentation

### Methods

#### `parse(data)`

**Description**: Parse the input data and return only error log lines.

**Arguments**:

- `data` (str): The log file content as a string.

**Returns**:

- `list`: List of error log lines.

---

## Usage

To use `ErrorParser`, instantiate it and call the `parse` method with log data.

```python
from langops.parser.error_parser import ErrorParser

parser = ErrorParser()
errors = parser.parse("log content here")
print(errors)
```
