import re

# GitHub Actions Patterns
GITHUB_ACTIONS_PATTERNS = {
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

GITHUB_ACTIONS_STAGE_PATTERNS = [
    re.compile(r"\[github\]\s+job\s+'(.+?)'", re.IGNORECASE),
    re.compile(r"\[github\]\s+step\s+'(.+?)'", re.IGNORECASE),
    re.compile(r"\[github\]\s+run\s+'(.+?)'", re.IGNORECASE),
    re.compile(r"\[github\]\s+Running\s+(?:job|step)\s+'(.+?)'", re.IGNORECASE),
    re.compile(r"::group::\s*(.+)", re.IGNORECASE),
    re.compile(r"##\[[a-z]+\]\s*Starting:\s*(.+)", re.IGNORECASE),
    re.compile(
        r"\[\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[.,]?\d*\]\s+\[INFO\]\s+Stage:\s+(.+)",
        re.IGNORECASE,
    ),
]
