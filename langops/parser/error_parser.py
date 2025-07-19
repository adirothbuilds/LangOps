from langops.core.base_parser import BaseParser
from langops.parser.registry import ParserRegistry
from typing import List, Dict, Any


@ParserRegistry.register(name="ErrorParser")
class ErrorParser(BaseParser):
    """Parser that filters and returns only error logs from the input data."""

    def parse(self, data: str) -> List[str]:
        """Parse the input data and return only error log lines.

        Args:
            data (str): The log file content as a string.

        Returns:
            list: List of error log lines.
        """
        import re

        self.validate_input(data)
        error_lines = self.filter_log_lines(
            data, pattern=r"\berr(or)?\b", flags=re.IGNORECASE
        )
        if not error_lines:
            error_lines = self.filter_log_lines(
                data, pattern=r"err|error", flags=re.IGNORECASE
            )
        return error_lines

    @classmethod
    def to_dict(cls, parsed_result: List[str]) -> Dict[str, Any]:
        """Convert the list of error log lines to a dictionary.

        Args:
            parsed_result (list): List of error log lines.

        Returns:
            dict: Dictionary with error log lines under the 'errors' key.
        """
        return {"errors": parsed_result}
