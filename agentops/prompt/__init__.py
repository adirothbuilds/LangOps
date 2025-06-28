from agentops.prompt.registry import PromptRegistry
from agentops.prompt.jenkins_error_prompt import JenkinsErrorPrompt

__name__ = "agentops.prompt"
__version__ = "0.1.0"
__author__ = "Adi Roth"
__license__ = "MIT"
__description__ = (
    "AgentOps Prompt: A module for integrating and managing prompt components in AI-driven workflows. "
    "Designed for extensibility and modularity, supporting registries and prompt templates."
)
__all__ = ["PromptRegistry", "JenkinsErrorPrompt"]
