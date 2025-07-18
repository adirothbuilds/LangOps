from typing import Type, Dict, Optional, Callable, List

# Alert registry for langops.alert


class AlertRegistry:
    """
    Registry for alert classes. Allows registration and retrieval of alerts by name.
    """

    _registry: Dict[str, Type] = {}

    @classmethod
    def register(cls, name: Optional[str] = None) -> Callable[[Type], Type]:
        """
        Decorator to register an alert class with an optional name.

        Args:
            name (str, optional): Name to register the alert under. If not provided, the class name is used.

        Returns:
            function: Decorator that registers the alert class.
        """

        def decorator(alert_cls: Type) -> Type:
            key = name or alert_cls.__name__
            cls._registry[key] = alert_cls
            return alert_cls

        return decorator

    @classmethod
    def get_alert(cls, name: str) -> Optional[Type]:
        """
        Retrieve an alert class by name.

        Args:
            name (str): Name of the alert class.

        Returns:
            type: The alert class if found, else None.
        """
        return cls._registry.get(name)

    @classmethod
    def list_alerts(cls) -> List[str]:
        """
        List all registered alert names.

        Returns:
            list: List of registered alert names as strings.
        """
        return list(cls._registry.keys())
