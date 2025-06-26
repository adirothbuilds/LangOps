# PromptRole

The `PromptRole` enum defines the roles available for prompt messages.

## Roles

- `system`: Represents system-level instructions.
- `user`: Represents user-provided input.
- `assistant`: Represents assistant-generated responses.

## Usage

Use the `PromptRole` enum to specify roles for prompt messages:

```python
from agentops.prompt.constants import PromptRole

role = PromptRole.system
```
