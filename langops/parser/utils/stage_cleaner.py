import re
from typing import Optional, Callable, Dict


def default_clean_stage_name(stage_name: str) -> Optional[str]:
    """
    Cleans the stage name by stripping whitespace and checking its length.

    Args:
        stage_name (str): The stage name to clean.

    Returns:
        Optional[str]: The cleaned stage name or None if invalid.
    """
    stage_name = stage_name.strip()
    if not stage_name or len(stage_name) < 2:
        return None
    return stage_name


def github_clean_stage_name(stage_name: str) -> Optional[str]:
    """
    Cleans stage names from GitHub Actions logs.

    Args:
        stage_name (str): The GitHub Actions stage name.

    Returns:
        Optional[str]: Cleaned stage name or None if invalid.
    """
    stage_name = stage_name.strip()
    stage_name = re.sub(r"^##\[group\]\s*", "", stage_name, flags=re.IGNORECASE)
    stage_name = re.sub(r"^Run\s+", "", stage_name, flags=re.IGNORECASE)

    if not stage_name or len(stage_name) < 2:
        return None
    return stage_name


def gitlab_clean_stage_name(stage_name: str) -> Optional[str]:
    """
    Cleans stage names from GitLab CI logs.

    Args:
        stage_name (str): The GitLab stage name.

    Returns:
        Optional[str]: Cleaned stage name or None if invalid.
    """
    stage_name = stage_name.strip()
    stage_name = re.sub(
        r"^----->\s*Running stage:\s*", "", stage_name, flags=re.IGNORECASE
    )
    stage_name = re.sub(r"^section_start:\d+:\s*", "", stage_name, flags=re.IGNORECASE)
    stage_name = re.sub(r"\[.*\]$", "", stage_name, flags=re.IGNORECASE)

    if not stage_name or len(stage_name) < 2:
        return None
    return stage_name


def jenkins_clean_stage_name(stage_name: str) -> Optional[str]:
    """
    Cleans the Jenkins stage name by removing common artifacts and checking for invalid names.

    Args:
        stage_name (str): The Jenkins stage name to clean.

    Returns:
        Optional[str]: The cleaned stage name or None if invalid.
    """
    stage_name = stage_name.strip()
    if stage_name.lower() in {"user", "admin", "system", "sh"}:
        return None
    stage_name = re.sub(r"^\d+[\.\)]\s*", "", stage_name)
    stage_name = re.sub(r"\s*\[.*?\]$", "", stage_name)
    return "Pipeline" if stage_name.lower() == "pipeline" else stage_name


STAGE_NAME_CLEANERS: Dict[str, Callable[[str], Optional[str]]] = {
    "github_actions": github_clean_stage_name,
    "gitlab_ci": gitlab_clean_stage_name,
    "jenkins": jenkins_clean_stage_name,
    "default": default_clean_stage_name,
}
