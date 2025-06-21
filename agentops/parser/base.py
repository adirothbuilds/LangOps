from abc import ABC, abstractmethod
import json


class BaseParser(ABC):
    """
    Abstract base class for all parsers.

    Provides utility methods for file handling, filtering, validation, and serialization.
    """

    @abstractmethod
    def parse(self, data):
        """
        Parse the input data and return the result.

        Args:
            data (Any): The data to be parsed.

        Returns:
            Any: The parsed result.
        """
        pass

    @staticmethod
    def handle_log_file(log_file_path):
        """
        Reads and returns the content of the log file.

        Args:
            log_file_path (str): Path to the log file.

        Returns:
            str: Content of the log file.
        """
        with open(log_file_path, "r", encoding="utf-8") as f:
            return f.read()

    @staticmethod
    def filter_log_lines(log_content, keyword=None, level=None, pattern=None, flags=0):
        """
        Filter log lines by keyword, log level, or regex pattern.

        Args:
            log_content (str): The content of the log file.
            keyword (str, optional): Keyword to filter lines. Defaults to None.
            level (str, optional): Log level to filter lines (e.g., 'ERROR', 'INFO'). Defaults to None.
            pattern (str, optional): Regex pattern to filter lines. Defaults to None.
            flags (int, optional): Regex flags (e.g., re.IGNORECASE). Defaults to 0.

        Returns:
            list: Filtered log lines.
        """
        import re

        lines = log_content.splitlines()
        filtered = []
        for line in lines:
            if pattern and not re.search(pattern, line, flags):
                continue
            if keyword and keyword not in line:
                continue
            if level and level not in line:
                continue
            filtered.append(line)
        return filtered

    @classmethod
    def validate_input(cls, data):
        """
        Validate input data. Override for custom validation in subclasses.

        Args:
            data (Any): Input data to validate.

        Raises:
            ValueError: If data is None or not a string.

        Returns:
            bool: True if valid.
        """
        if data is None or not isinstance(data, str):
            raise ValueError("Input data must be a non-empty string.")
        return True

    @classmethod
    def from_file(cls, file_path, *args, **kwargs):
        """
        Parse data directly from a file path. Must be called from a concrete subclass.

        Args:
            file_path (str): Path to the file.
            *args: Arguments for subclass constructor.
            **kwargs: Keyword arguments for subclass constructor.

        Raises:
            NotImplementedError: If called on BaseParser directly.

        Returns:
            Any: Parsed result from the file.
        """
        if cls is BaseParser:
            raise NotImplementedError(
                "from_file must be called from a subclass of BaseParser."
            )
        data = cls.handle_log_file(file_path)
        return cls(*args, **kwargs).parse(data)

    @classmethod
    def to_dict(cls, parsed_result):
        """
        Convert parsed result to a dictionary if possible. Override for custom serialization.

        Args:
            parsed_result (Any): The result to convert.

        Raises:
            TypeError: If conversion is not possible.

        Returns:
            dict: Dictionary representation of the parsed result.
        """
        if hasattr(parsed_result, "to_dict"):
            return parsed_result.to_dict()
        if isinstance(parsed_result, dict):
            return parsed_result
        if hasattr(parsed_result, "__dict__"):
            return vars(parsed_result)
        raise TypeError("Parsed result cannot be converted to dict.")

    @classmethod
    def to_json(cls, parsed_result):
        """
        Convert parsed result to a JSON string. Override for custom serialization.

        Args:
            parsed_result (Any): The result to convert.

        Raises:
            NotImplementedError: If called on BaseParser directly.
            ValueError: If conversion to JSON fails.

        Returns:
            str: JSON string representation of the parsed result.
        """
        if cls is BaseParser:
            raise NotImplementedError(
                "to_json must be called from a subclass of BaseParser."
            )
        try:
            dict_result = cls.to_dict(parsed_result)
            return json.dumps(dict_result, indent=2, ensure_ascii=False, sort_keys=True)
        except TypeError as e:
            raise ValueError(f"Failed to convert to JSON: {e}")
