from langops.core.base_prompt import BasePrompt
from langops.core.types import PromptRole
from langops.prompt.registry import PromptRegistry
from typing import List, Any


@PromptRegistry.register(name="JenkinsErrorPrompt")
class JenkinsErrorPrompt(BasePrompt):
    """
    Subclass of BasePrompt to handle error logs from Jenkins builds.
    """

    def __init__(self, build_id: str, timestamp: str, **kwargs: Any) -> None:
        """
        Initialize the JenkinsErrorPrompt instance with a system prompt.

        Args:
            build_id (str): The ID of the Jenkins build.
            timestamp (str): The timestamp of the error occurrence.
            **kwargs: Additional arguments for the BasePrompt.
        """
        super().__init__(**kwargs)
        self.add_prompt(
            role=PromptRole.SYSTEM,
            template="Analyzing Jenkins Build Error Logs\nBuild ID: {build_id}\nTimestamp: {timestamp}",
            variables={"build_id": build_id, "timestamp": timestamp},
        )

    def add_user_prompt(self, error_logs: List[str]) -> None:
        """
        Add a user prompt with error logs.

        Args:
            error_logs (list): List of error log messages.
        """
        for log in error_logs:
            self.add_prompt(
                role=PromptRole.USER,
                template="Error Log: {log}",
                variables={"log": log},
            )
