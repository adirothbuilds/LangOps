# BaseAlert

## Overview

`BaseAlert` is an abstract base class for all alerting mechanisms. It provides utility methods for formatting and sending alerts.

## API Documentation

### Methods

#### `format_alert(data)`

**Description**: Format the input data into the structure required for the alert.

**Arguments**:

- `data` (Any): The data to be formatted.

**Returns**:

- `Any`: The formatted alert structure.

---

#### `send_alert(formatted_data)`

**Description**: Send the alert using the formatted data.

**Arguments**:

- `formatted_data` (Any): The formatted alert data.

**Returns**:

- None

---

#### `validate_input(data)`

**Description**: Validate input data. Override for custom validation in subclasses.

**Arguments**:

- `data` (Any): Input data to validate.

**Raises**:

- `ValueError`: If data is None or not a dictionary.

**Returns**:

- `bool`: True if valid.

---

#### `from_data(data, *args, **kwargs)`

**Description**: Process data directly and send an alert. Must be called from a concrete subclass.

**Arguments**:

- `data` (dict): Data to process.
- `*args`: Arguments for subclass constructor.
- `**kwargs`: Keyword arguments for subclass constructor.

**Raises**:

- `NotImplementedError`: If called on BaseAlert directly.

**Returns**:

- Any: The result of the `send_alert` method.

---

## Usage

To implement a custom alert mechanism, inherit from `BaseAlert` and override the required methods.

```python
from langops.core.base_alert import BaseAlert

class CustomAlert(BaseAlert):
    def format_alert(self, data):
        return f"Alert: {data}"

    def send_alert(self, formatted_data):
        print(formatted_data)
```
