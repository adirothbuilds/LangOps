from typing import TypedDict


class RenderedPrompt(TypedDict):
    """
    Type definition for rendered prompts.
    """

    role: str
    content: str
