import re

# Azure DevOps Patterns – using common patterns by language
AZURE_DEVOPS_PATTERNS = {
    "python": "common.python",
    "nodejs": "common.nodejs",
    "java": "common.java",
    "dotnet": "common.dotnet",
    "shell": "common.shell",
    "batch": "common.batch",
    "docker": "common.docker",
    "kubernetes": "common.kubernetes",
    "make": "common.make",
}

AZURE_DEVOPS_STAGE_PATTERNS = [
    # Match typical Azure DevOps stage/step logs
    re.compile(r"^##\[group\]Starting: (.+)", re.IGNORECASE),
    re.compile(r"^##\[section\]Starting: (.+)", re.IGNORECASE),
    re.compile(r"^##\[stage\]Starting: (.+)", re.IGNORECASE),
    re.compile(r"^##\[step\]Starting: (.+)", re.IGNORECASE),
    re.compile(r"^##\[task\] (.+)", re.IGNORECASE),
    re.compile(r"^\[command\] (.+)", re.IGNORECASE),
    re.compile(r"^Starting: (.+)", re.IGNORECASE),
]
