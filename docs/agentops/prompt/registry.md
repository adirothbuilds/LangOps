# PromptRegistry

The `PromptRegistry` class provides a registry for managing different prompt classes.

## Methods

### `register(name, prompt_class)`

Registers a prompt class with a given name.

- **Args**:
  - `name (str)`: The name of the prompt class.
  - `prompt_class (Type[BasePrompt])`: The prompt class to register.
- **Raises**:
  - `ValueError`: If the name is already registered.

### `get(name)`

Retrieves a registered prompt class by name.

- **Args**:
  - `name (str)`: The name of the prompt class.
- **Returns**:
  - `Type[BasePrompt]`: The registered prompt class.

## Usage

To register a prompt class:

```python
PromptRegistry.register("custom", CustomPrompt)
```

To retrieve a registered prompt class:

```python
prompt_class = PromptRegistry.get("custom")
```
