from agentops.llm.registry import LLMRegistry
from agentops.llm.openai_llm import OpenAILLM

__name__ = "agentops.llm"
__version__ = "0.1.0"
__author__ = "Adi Roth"
__license__ = "MIT"
__description__ = (
    "AgentOps LLM: A module for integrating and managing Large Language Models (LLMs). "
    "Designed for extensibility and modularity, supporting decorators, registries, "
    "and OpenAI LLM integration."
)
__all__ = ["LLMRegistry", "OpenAILLM"]
