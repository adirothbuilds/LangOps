import re

# GitLab CI Patterns (language-level severity mapping)
GITLAB_CI_PATTERNS = {
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

# GitLab CI Stage Patterns
GITLAB_CI_STAGE_PATTERNS = [
    re.compile(
        r"\[\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[.,]?\d*\]\s+\[INFO\]\s+Stage:\s+(.+)",
        re.IGNORECASE,
    ),
    re.compile(r"Running with gitlab-runner", re.IGNORECASE),
    re.compile(r"Executing \"(.+?)\" stage of the job", re.IGNORECASE),
    re.compile(r"section_(start|end):\d+:[a-zA-Z0-9_-]+", re.IGNORECASE),
    re.compile(r"\[gitlab\]\s+\{\s*\((.+?)\)\}", re.IGNORECASE),
    re.compile(r"\[gitlab\]\s+(.+)", re.IGNORECASE),
]
