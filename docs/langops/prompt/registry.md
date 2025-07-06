# PromptRegistry

## Overview

`PromptRegistry` is a central hub for managing prompt classes. It allows registration and retrieval of prompts by name.

## API Documentation

### Methods

#### `register(name=None)`

**Description**: Decorator to register a prompt class with an optional name.

**Arguments**:

- `name` (str, optional): Name to register the prompt under. If not provided, the class name is used.

**Returns**:

- `function`: Decorator that registers the prompt class.

**Examples**:

```python
from langops.prompt.registry import PromptRegistry

@PromptRegistry.register(name="CustomPrompt")
class CustomPrompt:
    pass

# Retrieve the prompt
prompt_cls = PromptRegistry.get_prompt("CustomPrompt")
prompt_instance = prompt_cls()
```

#### `get_prompt(name)`

**Description**: Retrieve a prompt class by name.

**Arguments**:

- `name` (str): Name of the prompt class.

**Returns**:

- `type`: The prompt class if found, else None.

**Examples**:

```python
from langops.prompt.registry import PromptRegistry

prompt_cls = PromptRegistry.get_prompt("CustomPrompt")
prompt_instance = prompt_cls()
```

#### `list_prompts()`

**Description**: List all registered prompt names.

**Returns**:

- `list`: List of registered prompt names.

**Examples**:

```python
from langops.prompt.registry import PromptRegistry

print(PromptRegistry.list_prompts())
```

---

## Usage

To register a prompt, use the `@PromptRegistry.register` decorator. To retrieve a prompt, use the `get_prompt` method.

```python
from langops.prompt.registry import PromptRegistry

@PromptRegistry.register(name="JenkinsErrorPrompt")
class JenkinsErrorPrompt:
    pass

jenkins_prompt_cls = PromptRegistry.get_prompt("JenkinsErrorPrompt")
jenkins_prompt_instance = jenkins_prompt_cls()
```

---

## Integration

`PromptRegistry` integrates seamlessly with other modules like `JenkinsErrorPrompt`. For example, you can register `JenkinsErrorPrompt` and use it in a pipeline for prompt-based tasks.
