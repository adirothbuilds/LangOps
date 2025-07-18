from abc import ABC, abstractmethod
from typing import Dict, Optional, Any
from langops.core.types import LLMResponse


class BaseLLM(ABC):
    """
    Abstract base class for LLM model interaction.

    This interface allows switching between different LLM providers by implementing this class.
    Supports both synchronous and asynchronous completion methods.
    """

    @abstractmethod
    def complete(self, prompt: str, **kwargs: Any) -> LLMResponse:  # pragma: no cover
        """
        Synchronously generate a completion for the given prompt.

        Args:
            prompt (str): The input prompt for the LLM.
            **kwargs: Additional provider-specific arguments.

        Returns:
            LLMResponse: The structured response from the LLM.
        """
        pass

    async def acomplete(
        self, prompt: str, **kwargs: Any
    ) -> LLMResponse:  # pragma: no cover
        """
        Asynchronously generate a completion for the given prompt.

        Args:
            prompt (str): The input prompt for the LLM.
            **kwargs: Additional provider-specific arguments.

        Returns:
            LLMResponse: The structured response from the LLM.

        Raises:
            NotImplementedError: If async completion is not implemented by the subclass.
        """
        raise NotImplementedError(
            "Async completion is not implemented for this LLM client."
        )

    @staticmethod
    def format_prompt(base_prompt: str, variables: Optional[Dict[str, str]]) -> str:
        """
        Helper to inject variables into a base prompt string.

        Args:
            base_prompt (str): The prompt template with placeholders.
            variables (Optional[Dict[str, str]]): Variables to inject into the prompt.

        Returns:
            str: The formatted prompt.
        """
        if variables:
            return base_prompt.format(**variables)
        return base_prompt

    @classmethod
    @abstractmethod
    def default_model(cls) -> str:  # pragma: no cover
        """
        Returns the default model name for this LLM provider.

        Returns:
            str: The default model name.
        """
        pass
