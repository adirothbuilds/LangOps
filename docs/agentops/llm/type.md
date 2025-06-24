# Type Definitions

## Overview
This module defines type annotations used across the LLM integration. These types ensure that the parameters passed to OpenAI's API are correctly formatted and validated.

## Types

### `ChatCompletionMessageParam`
Represents a single message in a chat completion request. This type is used to structure the messages exchanged between the user and the assistant.

#### Fields
- `role`: The role of the message sender (e.g., `system`, `user`, `assistant`).
- `content`: The content of the message, which can be instructions, questions, or responses.

#### Example
```python
message = {"role": "user", "content": "What's the weather like in Paris today?"}
```

### `ChatCompletionUserMessageParam`
Represents a user message in a chat completion request. This type is a specialized version of `ChatCompletionMessageParam` for user inputs.

#### Fields
- `role`: Always `user`.
- `content`: The content of the user message.

#### Example
```python
user_message = {"role": "user", "content": "Tell me a joke about AI."}
```

## Usage
These types are used in the `OpenAILLM` class to ensure proper type annotations for OpenAI message parameters. They help developers understand the expected structure of inputs and outputs when interacting with OpenAI's API.
