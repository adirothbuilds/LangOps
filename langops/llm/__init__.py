from langops.llm.registry import LLMRegistry
from langops.llm.openai_llm import OpenAILLM

__name__ = "langops.llm"
__version__ = "0.1.0"
__author__ = "Adi Roth"
__license__ = "MIT"
__description__ = (
    "langops LLM: A module for integrating and managing Large Language Models (LLMs). "
    "Designed for extensibility and modularity, supporting decorators, registries, "
    "and OpenAI LLM integration."
)
__all__ = ["LLMRegistry", "OpenAILLM"]
