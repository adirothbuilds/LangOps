# BaseLLM

## Overview

`BaseLLM` is an abstract base class for interacting with LLM models. It supports both synchronous and asynchronous completion methods.

## API Documentation

### Methods

#### `complete(prompt, **kwargs)`

**Description**: Synchronously generate a completion for the given prompt.

**Arguments**:

- `prompt` (str): The input prompt for the LLM.
- `**kwargs`: Additional arguments for the LLM provider.

**Returns**:

- [`LLMResponse`](types.md#llmresponse): The response from the LLM.

---

#### `acomplete(prompt, **kwargs)`

**Description**: Asynchronously generate a completion for the given prompt.

**Arguments**:

- `prompt` (str): The input prompt for the LLM.
- `**kwargs`: Additional arguments for the LLM provider.

**Returns**:

- [`LLMResponse`](types.md#llmresponse): The response from the LLM.

**Raises**:

- `NotImplementedError`: If async completion is not implemented by the subclass.

---

#### `format_prompt(base_prompt, variables)`

**Description**: Helper to inject variables into a base prompt string.

**Arguments**:

- `base_prompt` (str): The prompt template with placeholders.
- `variables` (Optional[Dict[str, str]]): Variables to inject into the prompt.

**Returns**:

- `str`: The formatted prompt.

---

#### `default_model()`

**Description**: Returns the default model name for this LLM provider.

**Returns**:

- `str`: The default model name.

---

## Usage

To implement a custom LLM provider, inherit from `BaseLLM` and override the required methods.

```python
from langops.core.base_llm import BaseLLM

class CustomLLM(BaseLLM):
    def complete(self, prompt, **kwargs):
        return LLMResponse(text="Mock response", metadata={})

    async def acomplete(self, prompt, **kwargs):
        return LLMResponse(text="Async mock response", metadata={})

    @classmethod
    def default_model(cls):
        return "custom-model"
```
