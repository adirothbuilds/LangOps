from langops.core.base_llm import BaseLLM
from langops.core.base_alert import BaseAlert
from langops.core.base_parser import BaseParser
from langops.core.base_prompt import BasePrompt
from langops.core.types import RenderedPrompt, LLMResponse, PromptRole

__name__ = "langops.core"
__version__ = "0.1.0"
__author__ = "Adi Roth"
__license__ = "MIT"
__description__ = (
    "langops Core: Foundational SDK for building AI-driven workflows and automations. "
    "Provides base classes for LLMs, Prompts, Parsers, and Alerts. "
    "Designed for extensibility and modularity, enabling easy creation of custom components. "
)
__all__ = [
    "BaseLLM",
    "BaseAlert",
    "BaseParser",
    "BasePrompt",
    "PromptRole",
    "RenderedPrompt",
    "LLMResponse",
]
