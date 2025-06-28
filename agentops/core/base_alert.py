from abc import ABC, abstractmethod


class BaseAlert(ABC):
    """
    Abstract base class for all alerting mechanisms.

    Provides utility methods for formatting and sending alerts.
    """

    @abstractmethod
    def format_alert(self, data):  # pragma: no cover
        """
        Format the input data into the structure required for the alert.

        Args:
            data (Any): The data to be formatted.

        Returns:
            Any: The formatted alert structure.
        """
        pass

    @abstractmethod
    def send_alert(self, formatted_data):  # pragma: no cover
        """
        Send the alert using the formatted data.

        Args:
            formatted_data (Any): The formatted alert data.

        Returns:
            None
        """
        pass

    @classmethod
    def validate_input(cls, data):
        """
        Validate input data. Override for custom validation in subclasses.

        Args:
            data (Any): Input data to validate.

        Raises:
            ValueError: If data is None or not a dictionary.

        Returns:
            bool: True if valid.
        """
        if data is None or not isinstance(data, dict):
            raise ValueError("Input data must be a non-empty dictionary.")
        return True

    @classmethod
    def from_data(cls, data, *args, **kwargs):
        """
        Process data directly and send an alert. Must be called from a concrete subclass.

        Args:
            data (dict): Data to process.
            *args: Arguments for subclass constructor.
            **kwargs: Keyword arguments for subclass constructor.

        Raises:
            NotImplementedError: If called on BaseAlert directly.

        Returns:
            Any: The result of the `send_alert` method, typically indicating the alert was sent successfully.
        """
        if cls is BaseAlert:
            raise NotImplementedError(
                "from_data must be called from a subclass of BaseAlert."
            )
        cls.validate_input(data)
        formatted_data = cls(*args, **kwargs).format_alert(data)
        return cls(*args, **kwargs).send_alert(formatted_data)
