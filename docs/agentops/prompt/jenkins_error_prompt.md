# JenkinsErrorPrompt

The `JenkinsErrorPrompt` class is a specialized prompt for handling Jenkins error logs.

## Features

- Separates system and user messages.
- Automatically initializes system messages with predefined templates.

## Methods

### `__init__(system_template, user_template, variables)`

Initializes the prompt with system and user templates.

- **Args**:
  - `system_template (str)`: Template for the system message.
  - `user_template (str)`: Template for the user message.
  - `variables (Dict[str, Any])`: Variables to substitute in the templates.

### `render()`

Renders the prompt messages into the format required by the LLM.

- **Returns**:
  - `List[Dict[str, str]]`: A list of dictionaries representing the rendered prompt messages.

## Usage

To use the `JenkinsErrorPrompt`:

```python
from agentops.prompt.jenkins_error_prompt import JenkinsErrorPrompt

prompt = JenkinsErrorPrompt(
    system_template="System message template",
    user_template="User message template",
    variables={"key": "value"}
)
rendered = prompt.render()
print(rendered)
```
