# BaseLLM Documentation

## Overview

`BaseLLM` is an abstract base class designed to provide a consistent interface for interacting with various LLM (Large Language Model) providers. It supports both synchronous and asynchronous completion methods, allowing flexibility in implementation.

### Abstract Methods

#### complete(self, prompt: str, **kwargs) -> LLMResponse

Synchronously generate a completion for the given prompt.

**Args:**
- `prompt` (str): The input prompt for the LLM.
- `**kwargs`: Additional provider-specific arguments.

**Returns:**
- `LLMResponse`: The structured response from the LLM.

#### default_model(cls) -> str

Returns the default model name for this LLM provider.

**Returns:**
- `str`: The default model name.

### Methods

#### acomplete(self, prompt: str, **kwargs) -> LLMResponse

Asynchronously generate a completion for the given prompt.

**Args:**
- `prompt` (str): The input prompt for the LLM.
- `**kwargs`: Additional provider-specific arguments.

**Returns:**
- `LLMResponse`: The structured response from the LLM.

**Raises:**
- `NotImplementedError`: If async completion is not implemented by the subclass.

#### format_prompt(base_prompt: str, variables: Optional[Dict[str, str]]) -> str

Helper to inject variables into a base prompt string.

**Args:**
- `base_prompt` (str): The prompt template with placeholders.
- `variables` (Optional[Dict[str, str]]): Variables to inject into the prompt.

**Returns:**
- `str`: The formatted prompt.

## Usage Example

```python
class MyLLM(BaseLLM):
    def complete(self, prompt: str, **kwargs):
        return LLMResponse(text="Hello, world!", raw=None, metadata={})

    @classmethod
    def default_model(cls):
        return "my-llm-model"

llm = MyLLM()
response = llm.complete("What is AI?")
print(response.text)
```
