from typing import Type, Dict, Optional

# Prompt registry for langops.prompt


class PromptRegistry:
    """
    Registry for prompt classes. Allows registration and retrieval of prompts by name.
    """

    _registry: Dict[str, Type] = {}

    @classmethod
    def register(cls, name: Optional[str] = None):
        """
        Decorator to register a prompt class with an optional name.

        Args:
            name (str, optional): Name to register the prompt under. If not provided, the class name is used.

        Returns:
            function: Decorator that registers the prompt class.
        """

        def decorator(prompt_cls):
            key = name or prompt_cls.__name__
            cls._registry[key] = prompt_cls
            return prompt_cls

        return decorator

    @classmethod
    def get_prompt(cls, name: str):
        """
        Retrieve a prompt class by name.

        Args:
            name (str): Name of the prompt class.

        Returns:
            type: The prompt class if found, else None.
        """
        return cls._registry.get(name)

    @classmethod
    def list_prompts(cls):
        """
        List all registered prompt names.

        Returns:
            list: List of registered prompt names as strings.
        """
        return list(cls._registry.keys())
