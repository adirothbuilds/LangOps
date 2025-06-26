# RenderedPrompt

The `RenderedPrompt` type represents the structure of a rendered prompt message.

## Structure

A `RenderedPrompt` is a dictionary with the following keys:

- `role (str)`: The role of the message.
- `content (str)`: The content of the message.

## Usage

Use the `RenderedPrompt` type to define the output of the `BasePrompt.render()` method:

```python
from agentops.prompt.type import RenderedPrompt

message: RenderedPrompt = {
    "role": "system",
    "content": "This is a system message."
}
```
