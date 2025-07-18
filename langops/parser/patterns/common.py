import re
from langops.parser.types.pipeline_types import SeverityLevel
from typing import Pattern


def _p(pattern: str, flags: int = re.IGNORECASE) -> Pattern[str]:
    return re.compile(pattern, flags)


COMMON_PATTERNS = {
    "python": [
        (_p(r"Traceback \(most recent call last\):"), SeverityLevel.ERROR),
        (_p(r"MemoryError"), SeverityLevel.CRITICAL),
        (_p(r"ModuleNotFoundError"), SeverityLevel.ERROR),
        (_p(r"SyntaxError:"), SeverityLevel.ERROR),
    ],
    "nodejs": [
        (_p(r"UnhandledPromiseRejectionWarning"), SeverityLevel.ERROR),
        (_p(r"TypeError:"), SeverityLevel.ERROR),
        (_p(r"ReferenceError:"), SeverityLevel.ERROR),
        (_p(r"RangeError:"), SeverityLevel.ERROR),
        (_p(r"SyntaxError:"), SeverityLevel.ERROR),
        (_p(r"ENOENT: no such file or directory"), SeverityLevel.ERROR),
        (_p(r"ECONNREFUSED"), SeverityLevel.WARNING),
        (_p(r"EADDRINUSE"), SeverityLevel.ERROR),
        (_p(r"Cannot find module"), SeverityLevel.ERROR),
        (_p(r"Error: listen EACCES"), SeverityLevel.ERROR),
        (_p(r"DeprecationWarning:"), SeverityLevel.WARNING),
        (_p(r"##\[error\]"), SeverityLevel.ERROR),  # Azure DevOps format
        (_p(r"##\[warning\]"), SeverityLevel.WARNING),  # Azure DevOps format
        (_p(r"error TS\d{4}:"), SeverityLevel.ERROR),  # TypeScript compiler errors
        (
            _p(r"✖ \d+ problems? \(\d+ errors?, \d+ warnings?\)"),
            SeverityLevel.WARNING,
        ),  # ESLint summary
        (
            _p(r"'.+' is defined but never used"),
            SeverityLevel.WARNING,
        ),  # ESLint warning
        (_p(r"undefined is not a function"), SeverityLevel.ERROR),
        (
            _p(r"Cannot read properties of undefined"),
            SeverityLevel.ERROR,
        ),  # LLM error context
    ],
    "java": [
        (_p(r"Exception in thread"), SeverityLevel.CRITICAL),
        (_p(r"java\.lang\.NullPointerException"), SeverityLevel.CRITICAL),
        (_p(r"java\.lang\.OutOfMemoryError"), SeverityLevel.CRITICAL),
        (_p(r"java\.lang\.ArrayIndexOutOfBoundsException"), SeverityLevel.ERROR),
        (_p(r"java\.lang\.IllegalArgumentException"), SeverityLevel.ERROR),
        (_p(r"java\.lang\.IllegalStateException"), SeverityLevel.ERROR),
        (_p(r"java\.lang\.ClassCastException"), SeverityLevel.ERROR),
        (_p(r"Caused by:"), SeverityLevel.ERROR),
        (_p(r"ExceptionMapper"), SeverityLevel.WARNING),
        (_p(r"java\.sql\.SQLException"), SeverityLevel.ERROR),
        (
            _p(r"org\.springframework\.beans\.factory\.BeanCreationException"),
            SeverityLevel.CRITICAL,
        ),
        (_p(r"org\.hibernate\.Exception"), SeverityLevel.ERROR),
    ],
    "dotnet": [
        (_p(r"System\.NullReferenceException"), SeverityLevel.CRITICAL),
        (_p(r"System\.OutOfMemoryException"), SeverityLevel.CRITICAL),
        (_p(r"System\.InvalidOperationException"), SeverityLevel.ERROR),
        (_p(r"System\.ArgumentException"), SeverityLevel.ERROR),
        (_p(r"System\.IO\.IOException"), SeverityLevel.WARNING),
    ],
    "shell": [
        (_p(r"command not found"), SeverityLevel.ERROR),
        (_p(r"syntax error"), SeverityLevel.ERROR),
        (_p(r"permission denied"), SeverityLevel.ERROR),
        (_p(r"No such file or directory"), SeverityLevel.ERROR),
        (_p(r"operation not permitted"), SeverityLevel.ERROR),
    ],
    "batch": [
        (_p(r"The system cannot find the file specified"), SeverityLevel.ERROR),
        (_p(r"Access is denied"), SeverityLevel.ERROR),
        (_p(r"Syntax error in command line"), SeverityLevel.ERROR),
        (
            _p(r"is not recognized as an internal or external command"),
            SeverityLevel.ERROR,
        ),
    ],
    "docker": [
        (_p(r"no such file or directory"), SeverityLevel.ERROR),
        (_p(r"failed to build"), SeverityLevel.CRITICAL),
        (_p(r"error response from daemon:"), SeverityLevel.CRITICAL),
        (_p(r"manifest for .* not found"), SeverityLevel.ERROR),
        (_p(r"unauthorized: authentication required"), SeverityLevel.ERROR),
        (_p(r"pull access denied"), SeverityLevel.ERROR),
    ],
    "kubernetes": [
        (_p(r"CrashLoopBackOff"), SeverityLevel.CRITICAL),
        (_p(r"ImagePullBackOff"), SeverityLevel.CRITICAL),
        (_p(r"Failed to pull image"), SeverityLevel.ERROR),
        (_p(r"MountVolume.SetUp failed"), SeverityLevel.ERROR),
        (_p(r"Back-off restarting failed container"), SeverityLevel.ERROR),
        (_p(r"liveness probe failed"), SeverityLevel.WARNING),
        (_p(r"readiness probe failed"), SeverityLevel.WARNING),
    ],
    "make": [
        (_p(r"make: \*\*\* .* Error \d+"), SeverityLevel.ERROR),
        (_p(r"missing separator"), SeverityLevel.ERROR),
        (_p(r"recursive variable"), SeverityLevel.WARNING),
        (_p(r"undefined reference to"), SeverityLevel.ERROR),
    ],
}
