# OpenAILLM

## Overview

`OpenAILLM` integrates OpenAI's Python package for synchronous and asynchronous LLM completions. It supports routing requests to the correct endpoint based on the model type and prompt format.

## API Documentation

### Attributes

#### `CHAT_MODELS`

**Description**: A set of model names that support chat completions.

**Type**: `set`

---

### Methods

#### `__init__(api_key=None, model=None)`

**Description**: Initializes the `OpenAILLM` instance.

**Arguments**:

- `api_key` (Optional[str]): The API key for OpenAI. Defaults to None.
- `model` (Optional[str]): The model name to use. Defaults to None.

**Returns**: None

**Examples**:

```python
from langops.llm.openai_llm import OpenAILLM

llm = OpenAILLM(api_key="your-api-key", model="gpt-4")
```

#### `_is_chat_model(model_name=None)`

**Description**: Determines whether the given model name supports chat completions.

**Arguments**:

- `model_name` (Optional[str]): The model name to check. Defaults to None.

**Returns**:

- `bool`: True if the model supports chat completions, False otherwise.

**Examples**:

```python
llm = OpenAILLM(api_key="your-api-key", model="gpt-4")
print(llm._is_chat_model("gpt-4"))
```

#### `complete(prompt)`

**Description**: Generates a synchronous completion for the given prompt.

**Arguments**:

- `prompt` (str): The input prompt for the model.

**Returns**:

- `LLMResponse`: The response from the model.

**Examples**:

```python
llm = OpenAILLM(api_key="your-api-key", model="gpt-4")
response = llm.complete("What is the capital of France?")
print(response.text)
```

#### `acomplete(prompt)`

**Description**: Generates an asynchronous completion for the given prompt.

**Arguments**:

- `prompt` (str): The input prompt for the model.

**Returns**:

- `LLMResponse`: The response from the model.

**Examples**:

```python
import asyncio
from langops.llm.openai_llm import OpenAILLM

async def main():
    llm = OpenAILLM(api_key="your-api-key", model="gpt-4")
    response = await llm.acomplete("What is the capital of France?")
    print(response.text)

asyncio.run(main())
```

---

## Usage

To use `OpenAILLM`, instantiate it with your OpenAI API key and model name. You can use the `complete` method for synchronous completions or the `acomplete` method for asynchronous completions.

```python
from langops.llm.openai_llm import OpenAILLM

llm = OpenAILLM(api_key="your-api-key", model="gpt-4")

# Synchronous completion
response = llm.complete("Hello, world!")
print(response.text)

# Asynchronous completion
import asyncio
async def main():
    response = await llm.acomplete("Hello, world!")
    print(response.text)

asyncio.run(main())
```

---

## Integration

`OpenAILLM` can be registered with `LLMRegistry` for seamless integration into pipelines.

```python
from langops.llm.registry import LLMRegistry
from langops.llm.openai_llm import OpenAILLM

@LLMRegistry.register(name="openai")
class OpenAILLM:
    pass

llm_cls = LLMRegistry.get_llm("openai")
llm_instance = llm_cls(api_key="your-api-key")
response = llm_instance.complete("Hello, world!")
print(response.text)
```
