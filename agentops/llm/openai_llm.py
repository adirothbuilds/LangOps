from agentops.llm.base import BaseLLM
from agentops.llm.type import LLMResponse
from agentops.llm.registry import LLMRegistry

import openai
from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletionUserMessageParam,
)
from typing import Optional, List, Union, Any, Dict, TypeVar, cast

T = TypeVar("T")


@LLMRegistry.register("OpenAILLM")
class OpenAILLM(BaseLLM):
    """
    LLM client for OpenAI models using the openai Python package (v1+).

    This class supports both synchronous and asynchronous completions using
    OpenAI's Client and AsyncClient. It automatically routes requests to the
    correct endpoint based on the model type and prompt format.

    Attributes:
        CHAT_MODELS (set): A set of model names that support chat completions.
        api_key (str): The API key for authenticating with OpenAI.
        model (str): The model name to use for completions.
        client (Client): The synchronous OpenAI client.
        async_client (AsyncClient): The asynchronous OpenAI client.
    """

    CHAT_MODELS = {"gpt-3.5-turbo", "gpt-4", "gpt-4-turbo", "gpt-3.5-turbo-instruct"}

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initializes the OpenAILLM instance.

        Args:
            api_key (Optional[str]): The API key for OpenAI. Defaults to None.
            model (Optional[str]): The model name to use. Defaults to None.
        """
        self.api_key = api_key or openai.api_key
        self.model = model or self.default_model()
        self.client = openai.Client(api_key=self.api_key)
        self.async_client = openai.AsyncClient(api_key=self.api_key)

    def _is_chat_model(self, model_name: Optional[str] = None) -> bool:
        """
        Determines whether the given model name supports chat completions.

        Args:
            model_name (Optional[str]): The model name to check. Defaults to None.

        Returns:
            bool: True if the model supports chat completions, False otherwise.
        """
        model = (model_name or self.model).lower()
        return any(m in model for m in self.CHAT_MODELS)

    def _prepare_messages(
        self, prompt: Union[str, List[ChatCompletionMessageParam]]
    ) -> Union[List[ChatCompletionMessageParam], str]:
        """
        Prepares messages for API calls based on the prompt type and model.

        Args:
            prompt (Union[str, List[ChatCompletionMessageParam]): The input prompt.

        Returns:
            Union[List[ChatCompletionMessageParam], str]: The prepared messages or prompt.
        """
        if self._is_chat_model():
            if isinstance(prompt, str):
                return [ChatCompletionUserMessageParam(role="user", content=prompt)]
            return prompt
        else:
            if isinstance(prompt, list):
                return "\n".join(
                    [
                        str(msg["content"]) if isinstance(msg, dict) and msg.get("content") else ""
                        for msg in prompt
                    ]
                )
            return prompt

    def _extract_text_from_response(self, response: Any) -> str:
        """
        Extracts text content from an OpenAI API response.

        Args:
            response (Any): The API response object.

        Returns:
            str: The extracted text content.
        """
        if not hasattr(response, "choices") or not response.choices:
            return ""

        choice = response.choices[0]

        if self._is_chat_model():
            return self._extract_chat_content(choice)
        return self._extract_non_chat_text(choice)

    def _extract_chat_content(self, choice: Any) -> str:
        """Extracts content for chat models."""
        if hasattr(choice, "message") and choice.message:
            if hasattr(choice.message, "content") and choice.message.content:
                return str(choice.message.content)
        return ""

    def _extract_non_chat_text(self, choice: Any) -> str:
        """Extracts text for non-chat models."""
        if hasattr(choice, "text") and choice.text:
            return str(choice.text)
        return ""

    def _create_metadata(self, response: Any) -> Dict[str, Any]:
        """
        Creates a metadata dictionary from an API response.

        Args:
            response (Any): The API response object.

        Returns:
            Dict[str, Any]: The metadata dictionary.
        """
        return {
            "model_used": self.model,
            "id": getattr(response, "id", None),
            "object": getattr(response, "object", None),
            "created": getattr(response, "created", None),
            "usage": getattr(response, "usage", None),
        }

    def complete(
        self, prompt: Union[str, List[ChatCompletionMessageParam]], **kwargs
    ) -> LLMResponse:
        """
        Synchronously generates a completion using OpenAI's API.

        Routes the request to the correct endpoint based on the model type
        and prompt format.

        Args:
            prompt (Union[str, List[ChatCompletionMessageParam]): The input prompt.
            **kwargs: Additional arguments for the API call.

        Returns:
            LLMResponse: The structured response from the API.
        """
        messages_or_prompt = self._prepare_messages(prompt)

        if self._is_chat_model():
            response = self.client.chat.completions.create(
                model=self.model,
                messages=cast(List[ChatCompletionMessageParam], messages_or_prompt),
                **kwargs
            )
        else:
            response = self.client.completions.create(
                model=self.model, prompt=cast(str, messages_or_prompt), **kwargs
            )

        text = self._extract_text_from_response(response)
        metadata = self._create_metadata(response)

        return LLMResponse(text=str(text or ""), raw=response, metadata=metadata)

    async def acomplete(
        self, prompt: Union[str, List[ChatCompletionMessageParam]], **kwargs
    ) -> LLMResponse:
        """
        Asynchronously generates a completion using OpenAI's API.

        Routes the request to the correct endpoint based on the model type
        and prompt format.

        Args:
            prompt (Union[str, List[ChatCompletionMessageParam]): The input prompt.
            **kwargs: Additional arguments for the API call.

        Returns:
            LLMResponse: The structured response from the API.
        """
        messages_or_prompt = self._prepare_messages(prompt)

        if self._is_chat_model():
            response = await self.async_client.chat.completions.create(
                model=self.model,
                messages=cast(List[ChatCompletionMessageParam], messages_or_prompt),
                **kwargs
            )
        else:
            response = await self.async_client.completions.create(
                model=self.model, prompt=cast(str, messages_or_prompt), **kwargs
            )

        text = self._extract_text_from_response(response)
        metadata = self._create_metadata(response)

        return LLMResponse(text=str(text or ""), raw=response, metadata=metadata)

    @classmethod
    def default_model(cls) -> str:
        """
        Returns the default OpenAI model name.

        Returns:
            str: The default model name.
        """
        return "gpt-3.5-turbo"
