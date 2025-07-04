# Registry

## Overview
The `registry` module provides functionality for managing and accessing registered LLM instances. This module is useful for applications that require multiple LLM instances with different configurations.

## Functions

### `register_llm`
Registers an LLM instance in the registry.

#### Parameters
- `name`: The name of the LLM instance. This should be a unique identifier.
- `llm`: The LLM instance to register. This can be any object that implements the `BaseLLM` interface.

#### Example
```python
from langops.llm.openai_llm import OpenAILLM

llm_instance = OpenAILLM(api_key="your-api-key")
register_llm("openai", llm_instance)
```

### `get_llm`
Retrieves a registered LLM instance from the registry.

#### Parameters
- `name`: The name of the LLM instance.

#### Returns
- The registered LLM instance.

#### Example
```python
llm_instance = get_llm("openai")
response = llm_instance.complete("Tell me a joke about AI.")
print(response.text)
```

### External Plugin Usage
The registry can be extended to support external plugins or integrations. For example, you can register custom LLM implementations provided by third-party libraries or frameworks.

#### Example
```python
from langops.llm.registry import LLMRegistry

@LLMRegistry.register("custom")
class CustomLLM(BaseLLM):
    def complete(self, prompt, **kwargs):
        # Custom implementation
        return LLMResponse(text="Custom response", raw=None, metadata={})

# Retrieve and use the custom LLM
llm_instance = get_llm("custom")
response = llm_instance.complete("Tell me a joke about AI.")
print(response.text)
```
