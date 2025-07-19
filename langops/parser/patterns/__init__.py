from langops.parser.patterns.common import COMMON_PATTERNS
from langops.parser.patterns.jenkins import JENKINS_PATTERNS, JENKINS_STAGE_PATTERNS
from langops.parser.patterns.github_actions import (
    GITHUB_ACTIONS_PATTERNS,
    GITHUB_ACTIONS_STAGE_PATTERNS,
)
from langops.parser.patterns.gitlab_ci import (
    GITLAB_CI_PATTERNS,
    GITLAB_CI_STAGE_PATTERNS,
)
from langops.parser.patterns.azure_devops import (
    AZURE_DEVOPS_PATTERNS,
    AZURE_DEVOPS_STAGE_PATTERNS,
)


# Mapping of predefined patterns to their sources
PATTERNS = {
    "jenkins": JENKINS_PATTERNS,
    "github_actions": GITHUB_ACTIONS_PATTERNS,
    "gitlab_ci": GITLAB_CI_PATTERNS,
    "azure_devops": AZURE_DEVOPS_PATTERNS,
    "common": COMMON_PATTERNS,
}

# Mapping of predefined stage patterns to their sources
STAGE_PATTERNS = {
    "jenkins": JENKINS_STAGE_PATTERNS,
    "github_actions": GITHUB_ACTIONS_STAGE_PATTERNS,
    "gitlab_ci": GITLAB_CI_STAGE_PATTERNS,
    "azure_devops": AZURE_DEVOPS_STAGE_PATTERNS,
}

__all__ = ["PATTERNS", "STAGE_PATTERNS"]
