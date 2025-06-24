# OpenAILLM

## Overview
The `OpenAILLM` class provides integration with OpenAI's language models, enabling both synchronous and asynchronous completion methods. It supports legacy string prompts and multi-role chat prompts. This class is designed to simplify interaction with OpenAI's API, providing helper methods for preparing messages, extracting text, and creating metadata.

## Methods

### `complete`
```python
complete(prompt: Union[str, List[Dict[str, str]]]) -> CompletionResponse
```
Executes a synchronous completion request to OpenAI's API.

#### Parameters
- `prompt`: A string or a list of dictionaries representing the chat prompt. For example:
  - String prompt: `"Tell me a joke about AI."`
  - Chat prompt: `[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "What's the weather like in Paris today?"}]`

#### Returns
- `CompletionResponse`: Contains the generated text and metadata. The `text` field contains the response from the model, and the `metadata` field includes additional information such as token usage.

#### Example
```python
response = llm.complete("Tell me a joke about AI.")
print(response.text)
print(response.metadata)
```

### `acomplete`
```python
acomplete(prompt: Union[str, List[Dict[str, str]]]) -> CompletionResponse
```
Executes an asynchronous completion request to OpenAI's API.

#### Parameters
- `prompt`: A string or a list of dictionaries representing the chat prompt. The format is identical to the `complete` method.

#### Returns
- `CompletionResponse`: Contains the generated text and metadata.

#### Example
```python
async_response = await llm.acomplete(chat_prompt)
print(async_response.text)
print(async_response.metadata)
```

## Helper Methods

### `_prepare_messages`
Prepares the messages for OpenAI API requests. This method converts user inputs into the format required by OpenAI's API.

### `_extract_text_from_response`
Extracts the text from the OpenAI API response. This method ensures that the response is parsed correctly and handles edge cases.

### `_create_metadata`
Creates metadata from the OpenAI API response. Metadata includes information such as token usage, model name, and request duration.

## Usage
Refer to the demo script `demo/openai_llm_demo.py` for usage examples. This script demonstrates how to use both synchronous and asynchronous methods, as well as how to handle different types of prompts.
