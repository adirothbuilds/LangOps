from langops.parser.registry import ParserRegistry
from langops.parser.error_parser import ErrorParser

__name__ = "langops.parser"
__version__ = "0.1.0"
__author__ = "Adi Roth"
__license__ = "MIT"
__description__ = (
    "langops Parser: A module for integrating and managing parsers in AI-driven workflows. "
    "Designed for extensibility and modularity, supporting registries and error handling."
)
__all__ = ["ParserRegistry", "ErrorParser"]
