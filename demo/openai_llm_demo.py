import os
import asyncio
from agentops.llm import OpenAILLM

TEXT_LABEL = "Text:"
METADATA_LABEL = "Metadata:"

# Set your OpenAI API key (or use environment variable)
API_KEY = os.getenv("OPENAI_API_KEY")

# Example 1: Simple string prompt (legacy completion)
llm = OpenAILLM(api_key=API_KEY)
response = llm.complete("Tell me a joke about AI.")
print("Legacy completion:")
print(TEXT_LABEL, response.text)
print(METADATA_LABEL, response.metadata)

# Example 2: Multi-role chat prompt (recommended for gpt-3.5-turbo and above)
chat_prompt = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What's the weather like in Paris today?"}
]
chat_response = llm.complete(chat_prompt)
print("\nChat completion:")
print(TEXT_LABEL, chat_response.text)
print(METADATA_LABEL, chat_response.metadata)

# Example 3: Async usage (requires Python 3.7+)
async def async_example():
    async_llm = OpenAILLM(api_key=API_KEY)
    async_response = await async_llm.acomplete(chat_prompt)
    print("\nAsync chat completion:")
    print(TEXT_LABEL, async_response.text)
    print(METADATA_LABEL, async_response.metadata)

asyncio.run(async_example())
