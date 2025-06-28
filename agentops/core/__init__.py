from agentops.core.base_llm import BaseLLM
from agentops.core.base_alert import BaseAlert
from agentops.core.base_parser import BaseParser
from agentops.core.base_prompt import BasePrompt
from agentops.core.types import RenderedPrompt, LLMResponse, PromptRole

__name__ = "agentops.core"
__version__ = "0.1.0"
__author__ = "Adi Roth"
__license__ = "MIT"
__description__ = (
    "AgentOps Core: Foundational SDK for building AI-driven workflows and automations. "
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
