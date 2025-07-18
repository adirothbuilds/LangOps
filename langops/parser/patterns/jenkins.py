import re
from langops.parser.types.pipeline_types import SeverityLevel

# Jenkins Patterns
JENKINS_PATTERNS = {
    "groovy": [
        (
            re.compile(r".*groovy\.lang\.MissingPropertyException.*", re.IGNORECASE),
            SeverityLevel.ERROR,
        ),
        (
            re.compile(r".*unable to resolve class.*", re.IGNORECASE),
            SeverityLevel.ERROR,
        ),
        (
            re.compile(r".*groovy\.lang\.MissingMethodException.*", re.IGNORECASE),
            SeverityLevel.ERROR,
        ),
        (
            re.compile(r".*groovy\.lang\.GroovyRuntimeException.*", re.IGNORECASE),
            SeverityLevel.ERROR,
        ),
        (
            re.compile(r".*java\.lang\.ClassCastException.*", re.IGNORECASE),
            SeverityLevel.ERROR,
        ),
        (
            re.compile(r".*java\.lang\.NullPointerException.*", re.IGNORECASE),
            SeverityLevel.CRITICAL,
        ),
        (re.compile(r".*No such property:.*", re.IGNORECASE), SeverityLevel.ERROR),
        (re.compile(r".*WorkflowScript.*", re.IGNORECASE), SeverityLevel.ERROR),
        (
            re.compile(
                r".*org\.codehaus\.groovy\.control\.MultipleCompilationErrorsException.*",
                re.IGNORECASE,
            ),
            SeverityLevel.CRITICAL,
        ),
        (
            re.compile(r".*Cannot invoke method.*on null object.*", re.IGNORECASE),
            SeverityLevel.ERROR,
        ),
        (
            re.compile(
                r".*groovy\.lang\.MissingMethodException: No signature of method.*",
                re.IGNORECASE,
            ),
            SeverityLevel.ERROR,
        ),
    ],
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

# Jenkins Stage Patterns
JENKINS_STAGE_PATTERNS = [
    re.compile(
        r"\[\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[.,]?\d*\]\s+\[INFO\]\s+Stage:\s+(.+)",
        re.IGNORECASE,
    ),
    re.compile(r"^\s*\[\s*Pipeline\s*\]\s*\{\s*stage\s*\(.+?\)", re.IGNORECASE),
    re.compile(r"^\s*\[\s*Pipeline\s*\]\s*stage\s*\('(.+?)'\)", re.IGNORECASE),
    re.compile(r"\[jenkins\]\s+Running stage\s+'(.+?)'", re.IGNORECASE),
    re.compile(r"\[jenkins\]\s+Entering stage\s+'(.+?)'", re.IGNORECASE),
    re.compile(r"\[jenkins\]\s+(.+?)", re.IGNORECASE),
    re.compile(
        r"^\s*\[\s*Pipeline\s*\]\s*echo\s+.*Starting\s+stage:\s+(.+)", re.IGNORECASE
    ),
]
