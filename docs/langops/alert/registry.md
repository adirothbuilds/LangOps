# AlertRegistry

The `AlertRegistry` class provides a registry for managing different alerting mechanisms.

## Methods

### `register(name, alert_class)`

Registers an alert class with a given name.

- **Args**:
  - `name (str)`: The name of the alert class.
  - `alert_class (Type[BaseAlert])`: The alert class to register.
- **Raises**:
  - `ValueError`: If the name is already registered.

### `get(name)`

Retrieves a registered alert class by name.

- **Args**:
  - `name (str)`: The name of the alert class.
- **Returns**:
  - `Type[BaseAlert]`: The registered alert class.

## Usage

To register an alert class:

```python
AlertRegistry.register("custom", CustomAlert)
```

To retrieve a registered alert class:

```python
alert_class = AlertRegistry.get("custom")
```
