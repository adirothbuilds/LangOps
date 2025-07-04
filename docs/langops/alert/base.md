# BaseAlert

The `BaseAlert` class is an abstract base class for all alerting mechanisms. It provides utility methods for formatting and sending alerts.

## Methods

### `format_alert(data)`

Abstract method to format the input data into the structure required for the alert.

- **Args**:
  - `data (Any)`: The data to be formatted.
- **Returns**:
  - `Any`: The formatted alert structure.

### `send_alert(formatted_data)`

Abstract method to send the alert using the formatted data.

- **Args**:
  - `formatted_data (Any)`: The formatted alert data.
- **Returns**:
  - `None`

### `validate_input(data)`

Validates input data to ensure it is a non-empty dictionary.

- **Args**:
  - `data (Any)`: Input data to validate.
- **Raises**:
  - `ValueError`: If data is None or not a dictionary.
- **Returns**:
  - `bool`: True if valid.

### `from_data(data, *args, **kwargs)`

Processes data directly, formats it, sends an alert, and returns the result of the `send_alert` method.

- **Args**:
  - `data (dict)`: Data to process.
  - `*args`: Arguments for subclass constructor.
  - `**kwargs`: Keyword arguments for subclass constructor.
- **Raises**:
  - `NotImplementedError`: If called on `BaseAlert` directly.
- **Returns**:
  - `Any`: The result of the `send_alert` method.
