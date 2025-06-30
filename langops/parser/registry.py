from typing import Type, Dict, Optional

# Parser registry for langops.parser


class ParserRegistry:
    """
    Registry for parser classes. Allows registration and retrieval of parsers by name.
    """

    _registry: Dict[str, Type] = {}

    @classmethod
    def register(cls, name: Optional[str] = None):
        """
        Decorator to register a parser class with an optional name.

        Args:
            name (str, optional): Name to register the parser under. If not provided, the class name is used.

        Returns:
            function: Decorator that registers the parser class.
        """

        def decorator(parser_cls):
            key = name or parser_cls.__name__
            cls._registry[key] = parser_cls
            return parser_cls

        return decorator

    @classmethod
    def get_parser(cls, name: str):
        """
        Retrieve a parser class by name.

        Args:
            name (str): Name of the parser class.

        Returns:
            type: The parser class if found, else None.
        """
        return cls._registry.get(name)

    @classmethod
    def list_parsers(cls):
        """
        List all registered parser names.

        Returns:
            list: List of registered parser names as strings.
        """
        return list(cls._registry.keys())
