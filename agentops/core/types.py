from enum import Enum
from typing import Any, Dict, Optional, TypedDict


# agentops.llm types:


class LLMResponse:
    """
    Structure for LLM model responses.

    Attributes:
        text (str): The main text output from the LLM.
        raw (Any): The raw response object from the LLM provider (can be any type).
        metadata (dict): Additional metadata such as latency, model used, token usage, etc.
    """

    def __init__(
        self, text: str, raw: Any = None, metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Args:
            text (str): The main text output from the LLM.
            raw (Any, optional): The raw response object from the LLM provider. Defaults to None.
            metadata (dict, optional): Additional metadata (e.g., latency, model_used, token_usage). Defaults to None.
        """
        self.text = text
        self.raw = raw
        self.metadata = metadata or {}


# agentops.prompt types:


class PromptRole(Enum):
    """
    Enum for all supported roles in LLM prompts.
    """

    ASSISTANT = "assistant"
    USER = "user"
    SYSTEM = "system"
    OTHER = "other"


class RenderedPrompt(TypedDict):
    """
    Type definition for rendered prompts.
    """

    role: str
    content: str
