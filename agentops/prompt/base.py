from abc import ABC
from pydantic import BaseModel, Field
from typing import Dict, Any, List
from .constants import PromptRole
from .type import RenderedPrompt


class BasePrompt(BaseModel, ABC):
    """
    Abstract base class for handling LLM prompts dynamically.

    Provides functionality for saving, using, and templating prompts with variables.
    """

    prompts: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="List of prompt messages with roles and templates",
    )

    def add_prompt(
        self, role: PromptRole, template: str, variables: Dict[str, Any] = {}
    ):
        """
        Add a new prompt message to the list.

        Args:
            role (PromptRole): Role for which the prompt is designed.
            template (str): Prompt template with placeholders for variables.
            variables (Dict[str, Any], optional): Variables to fill the template. Defaults to {}.
        """
        self.prompts.append(
            {"role": role, "template": template, "variables": variables or {}}
        )

    def render_prompts(self) -> List[RenderedPrompt]:
        """
        Render all prompts by replacing placeholders in their templates with actual variables.

        Returns:
            List[RenderedPrompt]: List of rendered prompts in the format {"role": role, "content": rendered_content}.
        """
        return [
            {
                "role": prompt["role"].value,
                "content": prompt["template"].format(**prompt["variables"]),
            }
            for prompt in self.prompts
        ]

    def clear_prompts(self):
        """
        Clear all prompt messages.
        """
        self.prompts.clear()
