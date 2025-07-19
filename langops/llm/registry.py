from typing import Type, Dict, Optional, Callable, List

# LLM registry for langops.llm


class LLMRegistry:
    """
    Registry for LLM subclasses. Allows registration and retrieval of LLMs by name.
    """

    _registry: Dict[str, Type] = {}

    @classmethod
    def register(cls, name: Optional[str] = None) -> Callable[[Type], Type]:
        """
        Decorator to register an LLM subclass with an optional name.

        Args:
            name (str, optional): Name to register the LLM under. If not provided, the class name is used.

        Returns:
            function: Decorator that registers the LLM subclass.
        """

        def decorator(llm_cls: Type) -> Type:
            key = name or llm_cls.__name__
            cls._registry[key] = llm_cls
            return llm_cls

        return decorator

    @classmethod
    def get_llm(cls, name: str) -> Optional[Type]:
        """
        Retrieve an LLM subclass by name.

        Args:
            name (str): Name of the LLM subclass.

        Returns:
            type: The LLM subclass if found, else None.
        """
        return cls._registry.get(name)

    @classmethod
    def list_llms(cls) -> List[str]:
        """
        List all registered LLM names.

        Returns:
            list: List of registered LLM names as strings.
        """
        return list(cls._registry.keys())
