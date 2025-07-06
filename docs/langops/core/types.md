# Types

## Overview

`types.py` defines shared types and data structures used across the LangOps SDK.

## API Documentation

### Classes

#### `LLMResponse`

**Description**: Structure for LLM model responses.

**Attributes**:

- `text` (str): The main text output from the LLM.
- `raw` (Any): The raw response object from the LLM provider.
- `metadata` (Optional[Dict[str, Any]]): Additional metadata such as latency, model used, token usage, etc.

---

#### `PromptRole`

**Description**: Enum for all supported roles in LLM prompts.

**Values**:

- `ASSISTANT`: Represents the assistant role.
- `USER`: Represents the user role.
- `SYSTEM`: Represents the system role.
- `OTHER`: Represents other roles.

---

#### `RenderedPrompt`

**Description**: Type definition for rendered prompts.

**Attributes**:

- `role` (str): The role of the prompt.
- `content` (str): The content of the prompt.

---

#### `SeverityLevel`

**Description**: Enum for severity levels in logs.

**Values**:

- `INFO`: Informational messages.
- `WARNING`: Warning messages.
- `ERROR`: Error messages.
- `CRITICAL`: Critical error messages.

---

#### `LogEntry`

**Description**: Represents a single log entry.

**Attributes**:

- `timestamp` (Optional[datetime]): The timestamp of the log entry.
- `message` (str): The log message.
- `severity` ([`SeverityLevel`](types.md#severitylevel)): The severity level of the log.

---

#### `StageLogs`

**Description**: Represents logs for a specific stage.

**Attributes**:

- `name` (str): The name of the stage.
- `logs` (list[LogEntry]): List of log entries for the stage.

---

#### `ParsedLogBundle`

**Description**: Represents a bundle of parsed logs.

**Attributes**:

- `stages` (list[StageLogs]): List of stages with their logs.

---

## Usage

Use these types to structure data exchanged with LLMs and parsers.

```python
from langops.core.types import LLMResponse, SeverityLevel

response = LLMResponse(text="Hello, world!", metadata={"latency": 0.5})
print(response.text)

severity = SeverityLevel.ERROR
print(severity)
```
