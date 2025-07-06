# BasePrompt

## Overview

`BasePrompt` is an abstract base class for handling LLM prompts dynamically. It provides functionality for saving, using, and templating prompts with variables.

## API Documentation

### Attributes

#### `prompts`

**Description**: List of prompt messages with roles and templates.

**Type**: `List[Dict[str, Any]]`

### Methods

#### `add_prompt(role, template, variables={})`

**Description**: Add a new prompt message to the list.

**Arguments**:

- `role` ([`PromptRole`](types.md#promptrole)): Role for which the prompt is designed.
- `template` (str): Prompt template with placeholders for variables.
- `variables` (Dict[str, Any], optional): Variables to fill the template.

**Returns**:

- None

---

#### `render_prompts()`

**Description**: Render all prompts by replacing placeholders in their templates with actual variables.

**Returns**:

- `List[RenderedPrompt]`: List of rendered prompts.

---

#### `clear_prompts()`

**Description**: Clear all prompt messages.

**Returns**:

- None

---

## Usage

To use `BasePrompt`, create a subclass and define custom prompt handling logic.

```python
from langops.core.base_prompt import BasePrompt

class CustomPrompt(BasePrompt):
    def add_prompt(self, role, template, variables={}):
        self.prompts.append({"role": role, "template": template, "variables": variables})

    def render_prompts(self):
        return super().render_prompts()
```
