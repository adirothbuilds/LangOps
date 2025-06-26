# agentops.prompt Documentation

Welcome to the documentation for the `agentops.prompt` module. This package provides a flexible and extensible framework for building, registering, and using prompts for LLMs.

## Overview

- **Abstract Base Class:** Define consistent prompt structures with `BasePrompt`.
- **Registry System:** Register and retrieve prompt classes dynamically.
- **Custom Prompts:** Easily extend the framework to create custom prompt mechanisms.

## Getting Started

- All prompts should inherit from `BasePrompt` and implement the `render` method.
- Register your prompt class with the `PromptRegistry` using the `register` method.
- Use the registry to retrieve and instantiate prompts by name.

## Documentation Index

- [BasePrompt](./base.md): Abstract base class for all prompt mechanisms.
- [PromptRegistry](./registry.md): Registry for managing prompt classes.
- [PromptRole](./constants.md): Enum for defining roles in prompt messages.
- [RenderedPrompt](./type.md): Type definition for rendered prompt messages.
- [JenkinsErrorPrompt](./jenkins_error_prompt.md): Specialized prompt for Jenkins error logs.

## Example Usage

```python
from agentops.prompt import PromptRegistry

# Retrieve a registered prompt class by name
PromptClass = PromptRegistry.get("custom")
prompt = PromptClass()
rendered = prompt.render()
print(rendered)
```

## Contributing

- Add new prompt classes in the `agentops/prompt/` directory.
- Document each prompt in a separate markdown file in this folder.
- Update this index as new prompts and features are added.

## Future Expansion

This module is designed to grow. Planned features include:

- More built-in prompt mechanisms
- Advanced prompt configuration utilities
- Integration with external LLM frameworks

---

## Tests Reference

Unit tests for all core prompt components are located in:

- `tests/agentops/prompt/test_baseprompt.py`
- `tests/agentops/prompt/test_registry.py`
- `tests/agentops/prompt/test_jenkins_error_prompt.py`

These tests ensure the reliability and correctness of the prompt framework. Please refer to them for usage examples and to guide your own test development.

For details on each component, see the linked documentation pages above.
