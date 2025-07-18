# AlertRegistry

## Overview

The `AlertRegistry` class provides a centralized registry for managing alert classes and notification channels in LangOps.

## Class Definition

```python
class AlertRegistry:
    """
    Registry for alert classes. Allows registration and retrieval of alerts by name.
    """
```

## Methods

### `register(name: Optional[str] = None)`

Decorator to register an alert class with an optional name.

**Parameters:**

- `name` (str, optional): Name to register the alert under. If not provided, the class name is used.

**Returns:**

- Decorator function for registering the alert class

**Example:**

```python
from langops.alert.registry import AlertRegistry
from langops.core.base_alert import BaseAlert

@AlertRegistry.register(name="custom_alert")
class CustomAlert(BaseAlert):
    def send(self, message, severity="INFO"):
        # Custom alert logic
        pass
```

### `get_alert(name: str)`

Retrieve a registered alert class by name.

**Parameters:**

- `name` (str): Name of the alert to retrieve

**Returns:**

- Alert class instance

**Raises:**

- `KeyError`: If the alert is not found in the registry

**Example:**

```python
# Get registered alert
alert = AlertRegistry.get_alert("custom_alert")
alert.send("Test message", severity="WARNING")
```

### `list_alerts()`

List all registered alert names.

**Returns:**

- `List[str]`: List of registered alert names

**Example:**

```python
# List all available alerts
alerts = AlertRegistry.list_alerts()
print(f"Available alerts: {alerts}")
```

## Usage Examples

### Basic Registration

```python
from langops.alert.registry import AlertRegistry
from langops.core.base_alert import BaseAlert

@AlertRegistry.register()
class EmailAlert(BaseAlert):
    def __init__(self, smtp_server, username, password):
        self.smtp_server = smtp_server
        self.username = username
        self.password = password
    
    def send(self, message, severity="INFO"):
        # Send email alert
        pass

# Use the alert
email_alert = AlertRegistry.get_alert("EmailAlert")
```

### Named Registration

```python
@AlertRegistry.register(name="slack")
class SlackAlert(BaseAlert):
    def send(self, message, severity="INFO"):
        # Send Slack notification
        pass

# Use with custom name
slack_alert = AlertRegistry.get_alert("slack")
```

## Registry Properties

- **Thread-safe**: Registry operations are thread-safe for concurrent usage
- **Global scope**: Single registry instance across the application
- **Type validation**: Ensures registered classes inherit from BaseAlert

## Error Handling

The registry includes proper error handling:

```python
try:
    alert = AlertRegistry.get_alert("nonexistent_alert")
except KeyError:
    print("Alert not found in registry")
```

---

## See Also

- [BaseAlert](../core/base_alert.md): Base class for all alert implementations
- [Alert Index](index.md): Overview of the alert module
