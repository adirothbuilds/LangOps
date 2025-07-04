import re
from langops.core.types import SeverityLevel

# Jenkins Stage Detection Patterns
STAGE_PATTERNS = [
    # Primary Jenkins stage markers - highest priority
    re.compile(
        r"\[([A-Za-z][A-Za-z0-9\s]*)\]\s+(.*)"
    ),  # [Git] Cloning..., [Poetry] Installing..., etc.
    # Traditional stage patterns
    re.compile(r"\[Pipeline\]\s+\{\s*\((.+?)\)"),  # [Pipeline] { (stage_name)
    # Pipeline stage markers
    re.compile(r"\[Pipeline\]\s+(.+)"),  # [Pipeline] sh, [Pipeline] stage, etc.
    re.compile(r"Stage\s+['\"](.+?)['\"]"),  # Stage "Build"
    re.compile(r"Running in (.+)$"),  # Running in Build
    re.compile(r"\+\s+(.+?)\s+\["),  # + Build [
    # Build step markers
    re.compile(r"Build step\s+['\"](.+?)['\"]"),  # Build step 'Execute shell'
]

# Pattern: (regex, severity)
GROOVY_PATTERNS = [
    (
        re.compile(r".*groovy.lang.MissingPropertyException.*", re.IGNORECASE),
        SeverityLevel.ERROR,
    ),
    (re.compile(r".*unable to resolve class.*", re.IGNORECASE), SeverityLevel.ERROR),
]

JAVA_PATTERNS = [
    (re.compile(r".*Exception in thread.*", re.IGNORECASE), SeverityLevel.CRITICAL),
    (
        re.compile(r".*java.lang.NullPointerException.*", re.IGNORECASE),
        SeverityLevel.CRITICAL,
    ),
    (
        re.compile(r".*java.lang.OutOfMemoryError.*", re.IGNORECASE),
        SeverityLevel.CRITICAL,
    ),
]

NODEJS_PATTERNS = [
    (
        re.compile(r".*UnhandledPromiseRejectionWarning.*", re.IGNORECASE),
        SeverityLevel.ERROR,
    ),
    (re.compile(r".*TypeError:.*", re.IGNORECASE), SeverityLevel.ERROR),
    (re.compile(r".*ReferenceError:.*", re.IGNORECASE), SeverityLevel.ERROR),
]

PYTHON_PATTERNS = [
    (
        re.compile(r".*Traceback \(most recent call last\):.*", re.IGNORECASE),
        SeverityLevel.ERROR,
    ),
    (re.compile(r".*MemoryError.*", re.IGNORECASE), SeverityLevel.CRITICAL),
    (re.compile(r".*ModuleNotFoundError.*", re.IGNORECASE), SeverityLevel.ERROR),
    (re.compile(r".*SyntaxError:.*", re.IGNORECASE), SeverityLevel.ERROR),
]

DOTNET_PATTERNS = [
    (
        re.compile(r".*System.NullReferenceException.*", re.IGNORECASE),
        SeverityLevel.CRITICAL,
    ),
    (
        re.compile(r".*System.OutOfMemoryException.*", re.IGNORECASE),
        SeverityLevel.CRITICAL,
    ),
    (
        re.compile(r".*CS\d{4}:.*", re.IGNORECASE),
        SeverityLevel.ERROR,
    ),  # compiler errors like CS1001
]

SH_PATTERNS = [
    (re.compile(r".*command not found.*", re.IGNORECASE), SeverityLevel.ERROR),
    (re.compile(r".*No such file or directory.*", re.IGNORECASE), SeverityLevel.ERROR),
    (re.compile(r".*permission denied.*", re.IGNORECASE), SeverityLevel.ERROR),
    (
        re.compile(r".*unexpected EOF while looking for.*", re.IGNORECASE),
        SeverityLevel.ERROR,
    ),
    (re.compile(r".*syntax error:.*", re.IGNORECASE), SeverityLevel.ERROR),
    (
        re.compile(r".*line \d+:.*", re.IGNORECASE),
        SeverityLevel.ERROR,
    ),  # Shell script line errors
]

# Jenkins-specific error patterns
JENKINS_PATTERNS = [
    (
        re.compile(r".*Build step.*marked build as FAILURE.*", re.IGNORECASE),
        SeverityLevel.CRITICAL,
    ),
    (re.compile(r".*FAILURE.*", re.IGNORECASE), SeverityLevel.ERROR),
    (re.compile(r".*ERROR.*", re.IGNORECASE), SeverityLevel.ERROR),
    (re.compile(r".*FAILED.*", re.IGNORECASE), SeverityLevel.ERROR),
    (re.compile(r".*marked build as UNSTABLE.*", re.IGNORECASE), SeverityLevel.WARNING),
]

# HTTP/Network error patterns
HTTP_PATTERNS = [
    (re.compile(r".*curl:.*returned error:.*", re.IGNORECASE), SeverityLevel.ERROR),
    (re.compile(r".*401 Unauthorized.*", re.IGNORECASE), SeverityLevel.ERROR),
    (re.compile(r".*403 Forbidden.*", re.IGNORECASE), SeverityLevel.ERROR),
    (re.compile(r".*404 Not Found.*", re.IGNORECASE), SeverityLevel.ERROR),
    (
        re.compile(r".*500 Internal Server Error.*", re.IGNORECASE),
        SeverityLevel.CRITICAL,
    ),
    (re.compile(r".*Connection refused.*", re.IGNORECASE), SeverityLevel.ERROR),
    (re.compile(r".*timeout.*", re.IGNORECASE), SeverityLevel.WARNING),
]

# Test failure patterns
TEST_PATTERNS = [
    (re.compile(r".*FAILURES.*", re.IGNORECASE), SeverityLevel.ERROR),
    (re.compile(r".*ValidationError:.*", re.IGNORECASE), SeverityLevel.ERROR),
    (re.compile(r".*field required.*", re.IGNORECASE), SeverityLevel.ERROR),
    (re.compile(r".*test.*failed.*", re.IGNORECASE), SeverityLevel.ERROR),
    (re.compile(r".*assertion.*error.*", re.IGNORECASE), SeverityLevel.ERROR),
]

# Linting error patterns
LINT_PATTERNS = [
    (
        re.compile(r".*:(\d+):(\d+):\s+([EWFCN]\d+)\s+(.*)"),
        SeverityLevel.WARNING,
    ),  # flake8 format
    (re.compile(r".*imported but unused.*", re.IGNORECASE), SeverityLevel.WARNING),
    (re.compile(r".*line too long.*", re.IGNORECASE), SeverityLevel.WARNING),
    (re.compile(r".*do not use bare.*except.*", re.IGNORECASE), SeverityLevel.WARNING),
]

SONAR_PATTERNS = [
    (
        re.compile(r".*SonarScanner.*execution failed.*", re.IGNORECASE),
        SeverityLevel.ERROR,
    ),
    (
        re.compile(r".*java.lang.IllegalStateException.*", re.IGNORECASE),
        SeverityLevel.ERROR,
    ),
]

JFROG_PATTERNS = [
    (re.compile(r".*xray scan failed.*", re.IGNORECASE), SeverityLevel.ERROR),
    (re.compile(r".*unauthorized.*", re.IGNORECASE), SeverityLevel.WARNING),
    (re.compile(r".*failed to resolve artifact.*", re.IGNORECASE), SeverityLevel.ERROR),
]

DOCKER_PATTERNS = [
    (re.compile(r".*no space left on device.*", re.IGNORECASE), SeverityLevel.CRITICAL),
    (re.compile(r".*manifest for .* not found.*", re.IGNORECASE), SeverityLevel.ERROR),
    (re.compile(r".*error response from daemon.*", re.IGNORECASE), SeverityLevel.ERROR),
    (re.compile(r".*failed to pull image.*", re.IGNORECASE), SeverityLevel.ERROR),
]
