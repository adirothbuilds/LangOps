# JenkinsErrorPrompt

## Overview

`JenkinsErrorPrompt` is a subclass of `BasePrompt` designed to handle error logs from Jenkins builds. It provides methods for initializing system prompts and adding user prompts with error logs.

## API Documentation

### Methods

#### `__init__(build_id, timestamp, **kwargs)`

**Description**: Initializes the `JenkinsErrorPrompt` instance with a system prompt.

**Arguments**:

- `build_id` (str): The ID of the Jenkins build.
- `timestamp` (str): The timestamp of the error occurrence.
- `**kwargs`: Additional arguments for the `BasePrompt`.

**Returns**: None

**Examples**:

```python
from langops.prompt.jenkins_error_prompt import JenkinsErrorPrompt

prompt = JenkinsErrorPrompt(build_id="12345", timestamp="2025-07-06")
```

#### `add_user_prompt(error_logs)`

**Description**: Adds a user prompt with error logs.

**Arguments**:

- `error_logs` (list): List of error log messages.

**Returns**: None

**Examples**:

```python
prompt = JenkinsErrorPrompt(build_id="12345", timestamp="2025-07-06")
error_logs = ["Error: Build failed", "Error: Timeout"]
prompt.add_user_prompt(error_logs)
```

---

## Usage

To use `JenkinsErrorPrompt`, instantiate it with the build ID and timestamp, and add user prompts with error logs.

```python
from langops.prompt.jenkins_error_prompt import JenkinsErrorPrompt

prompt = JenkinsErrorPrompt(build_id="12345", timestamp="2025-07-06")
error_logs = ["Error: Build failed", "Error: Timeout"]
prompt.add_user_prompt(error_logs)

# Access the prompt data
print(prompt.prompts)
```

---

## Integration

`JenkinsErrorPrompt` can be registered with `PromptRegistry` for seamless integration into pipelines.

```python
from langops.prompt.registry import PromptRegistry
from langops.prompt.jenkins_error_prompt import JenkinsErrorPrompt

@PromptRegistry.register(name="JenkinsErrorPrompt")
class JenkinsErrorPrompt:
    pass

prompt_cls = PromptRegistry.get_prompt("JenkinsErrorPrompt")
prompt_instance = prompt_cls(build_id="12345", timestamp="2025-07-06")
```
