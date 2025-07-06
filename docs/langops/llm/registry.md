# LLMRegistry

## Overview

`LLMRegistry` is a central hub for managing LLM subclasses. It allows registration and retrieval of LLMs by name.

## API Documentation

### Methods

#### `register(name=None)`

**Description**: Decorator to register an LLM subclass with an optional name.

**Arguments**:

- `name` (str, optional): Name to register the LLM under. If not provided, the class name is used.

**Returns**:

- `function`: Decorator that registers the LLM subclass.

**Examples**:

```python
from langops.llm.registry import LLMRegistry

@LLMRegistry.register(name="CustomLLM")
class CustomLLM:
    pass

# Retrieve the LLM
llm_cls = LLMRegistry.get_llm("CustomLLM")
llm_instance = llm_cls()
```

#### `get_llm(name)`

**Description**: Retrieve an LLM subclass by name.

**Arguments**:

- `name` (str): Name of the LLM subclass.

**Returns**:

- `type`: The LLM subclass if found, else None.

**Examples**:

```python
from langops.llm.registry import LLMRegistry

llm_cls = LLMRegistry.get_llm("CustomLLM")
llm_instance = llm_cls()
```

#### `list_llms()`

**Description**: List all registered LLM names.

**Returns**:

- `list`: List of registered LLM names.

**Examples**:

```python
from langops.llm.registry import LLMRegistry

print(LLMRegistry.list_llms())
```

---

## Usage

To register an LLM, use the `@LLMRegistry.register` decorator. To retrieve an LLM, use the `get_llm` method.

```python
from langops.llm.registry import LLMRegistry

@LLMRegistry.register(name="OpenAILLM")
class OpenAILLM:
    pass

openai_llm_cls = LLMRegistry.get_llm("OpenAILLM")
openai_llm_instance = openai_llm_cls()
```

---

## Integration

`LLMRegistry` integrates seamlessly with other modules like `OpenAILLM`. For example, you can register `OpenAILLM` and use it in a pipeline for LLM-based tasks.
