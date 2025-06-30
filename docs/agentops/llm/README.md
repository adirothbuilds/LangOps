# langops.llm Documentation

Welcome to the documentation for the `langops.llm` module. This package provides a flexible and extensible framework for integrating with various language models, including OpenAI's GPT models.

## Overview

- **Modular Design:** Easily extend the base LLM class to support new models and APIs.
- **Registry System:** Register and retrieve LLM instances dynamically using decorators.
- **Base Classes:** Abstract base classes and utilities for consistent LLM development.
- **OpenAI Integration:** Built-in support for OpenAI's GPT models with synchronous and asynchronous completions.

## Getting Started

- All LLM implementations should inherit from `BaseLLM` and implement the `complete` and `acomplete` methods.
- Register your LLM with the `LLMRegistry` using the `@LLMRegistry.register()` decorator.
- Use the registry to retrieve and instantiate LLMs by name.

## Documentation Index

- [BaseLLM](./base.md): Abstract base class and utilities for all LLM integrations.
- [OpenAILLM](./openai_llm.md): Integration with OpenAI's GPT models.
- [Type Definitions](./type.md): Type annotations for OpenAI message parameters.
- [Registry](./registry.md): Decorator-based registry for managing LLM instances.

## Example Usage

```python
from langops.llm.registry import get_llm

# Retrieve a registered LLM by name
llm_instance = get_llm('OpenAILLM')
response = llm_instance.complete("Tell me a joke about AI.")
print(response.text)
```

## Contributing

- Add new LLM classes in the `langops/llm/` directory.
- Document each LLM in a separate markdown file in this folder.
- Update this index as new LLMs and features are added.

## Future Expansion

This module is designed to grow. Planned features include:

- Support for additional language model APIs
- Advanced completion utilities
- LLM chaining and orchestration

---

## Tests Reference

Unit tests for all core LLM components are located in:

- `tests/langops/llm/test_base.py`
- `tests/langops/llm/test_openai_llm.py`
- `tests/langops/llm/test_registry.py`
- `tests/langops/llm/test_type.py`

These tests ensure the reliability and correctness of the LLM framework. Please refer to them for usage examples and to guide your own test development.

For details on each component, see the linked documentation pages above.
