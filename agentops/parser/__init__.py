from agentops.parser.registry import ParserRegistry
from agentops.parser.error_parser import ErrorParser

__name__ = "agentops.parser"
__version__ = "0.1.0"
__author__ = "Adi Roth"
__license__ = "MIT"
__description__ = (
    "AgentOps Parser: A module for integrating and managing parsers in AI-driven workflows. "
    "Designed for extensibility and modularity, supporting registries and error handling."
)
__all__ = ["ParserRegistry", "ErrorParser"]
