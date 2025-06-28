# Exposing Core Components
from agentops.core import BaseAlert, BaseParser, BasePrompt, BaseLLM

# Exposing Registries
from agentops.prompt.registry import PromptRegistry
from agentops.parser.registry import ParserRegistry
from agentops.llm.registry import LLMRegistry
from agentops.alert.registry import AlertRegistry

# Exposing types and constants
from agentops.core.types import LLMResponse, RenderedPrompt, PromptRole

__version__ = "0.1.0"
__author__ = "Adi Roth"
__license__ = "MIT"
__description__ = (
    "AgentOps: An SDK for building AI-driven workflows and automations as code. "
    "Provides extensible and modular support for LLMs, prompts, parsers, and alerts."
)

# Exposing Core Components
__all__ = [
    "BaseAlert",
    "BaseParser",
    "BasePrompt",
    "BaseLLM",
    "PromptRegistry",
    "ParserRegistry",
    "LLMRegistry",
    "AlertRegistry",
    "LLMResponse",
    "RenderedPrompt",
    "PromptRole",
]
