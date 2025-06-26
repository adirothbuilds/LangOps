# BasePrompt

The `BasePrompt` class provides a flexible framework for defining and rendering prompts for LLMs. It supports multi-role prompts, templates, and variable substitution.

## Attributes

### `messages`

A list of prompt messages, each with a role, template, and variables.

### `roles`

Defines the roles available for prompt messages (e.g., `system`, `user`, `assistant`).

## Methods

### `render()`

Renders the prompt messages into the format required by the LLM.

- **Returns**:
  - `List[Dict[str, str]]`: A list of dictionaries representing the rendered prompt messages.

### `add_message(role, template, variables)`

Adds a new message to the prompt.

- **Args**:
  - `role (str)`: The role of the message.
  - `template (str)`: The template for the message.
  - `variables (Dict[str, Any])`: Variables to substitute in the template.

## Usage

To create a custom prompt, extend the `BasePrompt` class and define specific templates and roles.
