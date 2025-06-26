from enum import Enum


class PromptRole(Enum):
    """
    Enum for all supported roles in LLM prompts.
    """

    ASSISTANT = "assistant"
    USER = "user"
    SYSTEM = "system"
    OTHER = "other"
