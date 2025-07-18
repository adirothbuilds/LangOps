# Common Patterns

## Overview

The `common.py` module provides a comprehensive set of error patterns that are shared across multiple CI/CD platforms and programming languages. These patterns form the foundation for error detection in pipeline logs.

## Pattern Structure

All patterns are organized by programming language or technology and follow this structure:

```python
COMMON_PATTERNS = {
    "language_name": [
        (compiled_regex, SeverityLevel.LEVEL),
        # More patterns...
    ],
    # More languages...
}
```

## Supported Languages and Technologies

### Python

Common Python error patterns for exceptions, import errors, and runtime issues.

**Patterns:**

- `Traceback (most recent call last):` - Python stack trace (ERROR)
- `MemoryError` - Memory allocation errors (CRITICAL)
- `ModuleNotFoundError` - Missing module imports (ERROR)
- `SyntaxError:` - Python syntax errors (ERROR)

**Example:**

```python
from langops.parser.patterns.common import COMMON_PATTERNS

python_patterns = COMMON_PATTERNS["python"]
# [(compiled_regex, SeverityLevel.ERROR), ...]
```

### Node.js/JavaScript

JavaScript and Node.js error patterns for runtime errors, type errors, and module issues.

**Patterns:**

- `UnhandledPromiseRejectionWarning` - Unhandled promise rejections (ERROR)
- `TypeError:` - Type-related errors (ERROR)
- `ReferenceError:` - Variable reference errors (ERROR)
- `RangeError:` - Range and bounds errors (ERROR)
- `ENOENT: no such file or directory` - File not found errors (ERROR)
- `ECONNREFUSED` - Connection refused errors (WARNING)
- `Cannot find module` - Module resolution errors (ERROR)
- `error TS\d{4}:` - TypeScript compiler errors (ERROR)

**Example:**

```python
from langops.parser.patterns.common import COMMON_PATTERNS

nodejs_patterns = COMMON_PATTERNS["nodejs"]
# Includes patterns for Node.js, TypeScript, and ESLint errors
```

### Java

Java application error patterns for exceptions, memory errors, and framework issues.

**Patterns:**

- `Exception in thread` - Thread exceptions (CRITICAL)
- `java.lang.NullPointerException` - Null pointer exceptions (CRITICAL)
- `java.lang.OutOfMemoryError` - Memory errors (CRITICAL)
- `java.lang.ArrayIndexOutOfBoundsException` - Array bounds errors (ERROR)
- `java.sql.SQLException` - Database errors (ERROR)
- `org.springframework.beans.factory.BeanCreationException` - Spring framework errors (CRITICAL)

**Example:**

```python
from langops.parser.patterns.common import COMMON_PATTERNS

java_patterns = COMMON_PATTERNS["java"]
# Includes JVM, Spring, and Hibernate error patterns
```

### .NET

.NET application error patterns for system exceptions and runtime errors.

**Patterns:**

- `System.NullReferenceException` - Null reference exceptions (CRITICAL)
- `System.OutOfMemoryException` - Memory allocation errors (CRITICAL)
- `System.InvalidOperationException` - Invalid operations (ERROR)
- `System.ArgumentException` - Argument validation errors (ERROR)
- `System.IO.IOException` - I/O operation errors (WARNING)

**Example:**

```python
from langops.parser.patterns.common import COMMON_PATTERNS

dotnet_patterns = COMMON_PATTERNS["dotnet"]
# Includes .NET Framework and .NET Core error patterns
```

### Shell/Bash

Shell script error patterns for command execution and system errors.

**Patterns:**

- `command not found` - Command execution errors (ERROR)
- `syntax error` - Shell syntax errors (ERROR)
- `permission denied` - Permission issues (ERROR)
- `No such file or directory` - File access errors (ERROR)
- `operation not permitted` - Operation permission errors (ERROR)

**Example:**

```python
from langops.parser.patterns.common import COMMON_PATTERNS

shell_patterns = COMMON_PATTERNS["shell"]
# Includes bash, sh, and zsh error patterns
```

### Batch (Windows)

Windows batch script error patterns for system and command errors.

**Patterns:**

- `The system cannot find the file specified` - File not found errors (ERROR)
- `Access is denied` - Permission errors (ERROR)
- `Syntax error in command line` - Command syntax errors (ERROR)
- `is not recognized as an internal or external command` - Command not found errors (ERROR)

**Example:**

```python
from langops.parser.patterns.common import COMMON_PATTERNS

batch_patterns = COMMON_PATTERNS["batch"]
# Includes Windows batch and PowerShell error patterns
```

### Docker

Docker container and image error patterns for build and runtime issues.

**Patterns:**

- `no such file or directory` - File system errors (ERROR)
- `failed to build` - Build process errors (CRITICAL)
- `error response from daemon:` - Docker daemon errors (CRITICAL)
- `manifest for .* not found` - Image manifest errors (ERROR)
- `unauthorized: authentication required` - Authentication errors (ERROR)
- `pull access denied` - Image pull permission errors (ERROR)

**Example:**

```python
from langops.parser.patterns.common import COMMON_PATTERNS

docker_patterns = COMMON_PATTERNS["docker"]
# Includes Docker build, run, and registry error patterns
```

### Kubernetes

Kubernetes deployment and pod error patterns for cluster issues.

**Patterns:**

- `CrashLoopBackOff` - Pod restart loop errors (CRITICAL)
- `ImagePullBackOff` - Image pull failures (CRITICAL)
- `Failed to pull image` - Image retrieval errors (ERROR)
- `MountVolume.SetUp failed` - Volume mounting errors (ERROR)
- `Back-off restarting failed container` - Container restart errors (ERROR)
- `liveness probe failed` - Health check failures (WARNING)
- `readiness probe failed` - Readiness check failures (WARNING)

**Example:**

```python
from langops.parser.patterns.common import COMMON_PATTERNS

k8s_patterns = COMMON_PATTERNS["kubernetes"]
# Includes pod, service, and deployment error patterns
```

### Make

GNU Make and build system error patterns for compilation and build issues.

**Patterns:**

- `make: \*\*\* .* Error \d+` - Make build errors (ERROR)
- `missing separator` - Makefile syntax errors (ERROR)
- `recursive variable` - Variable definition warnings (WARNING)
- `undefined reference to` - Linking errors (ERROR)

**Example:**

```python
from langops.parser.patterns.common import COMMON_PATTERNS

make_patterns = COMMON_PATTERNS["make"]
# Includes Make, CMake, and build system error patterns
```

## Usage Examples

### Direct Pattern Access

```python
from langops.parser.patterns.common import COMMON_PATTERNS

# Get all Python patterns
python_patterns = COMMON_PATTERNS["python"]

# Use in pattern matching
for pattern, severity in python_patterns:
    if pattern.search(log_line):
        print(f"Found {severity} error: {log_line}")
```

### Pattern Resolution

```python
from langops.parser.utils.resolver import PatternResolver

# Reference common patterns in configuration
config = {
    "python": "common.python",
    "nodejs": "common.nodejs",
    "docker": "common.docker"
}

resolver = PatternResolver()
resolved_patterns = resolver.resolve_patterns(config)
```

### Custom Pattern Extension

```python
from langops.parser.patterns.common import COMMON_PATTERNS
from langops.parser.types.pipeline_types import SeverityLevel
import re

# Add custom patterns to existing language
custom_python_patterns = [
    (re.compile(r"CustomError:", re.IGNORECASE), SeverityLevel.ERROR),
    (re.compile(r"CustomWarning:", re.IGNORECASE), SeverityLevel.WARNING),
]

# Extend existing patterns
COMMON_PATTERNS["python"].extend(custom_python_patterns)
```

## Pattern Helper Function

### `_p(pattern: str, flags=re.IGNORECASE) -> re.Pattern`

A helper function that compiles regex patterns with consistent flags.

**Parameters:**

- `pattern` (str): The regex pattern string
- `flags` (int, optional): Regex flags (default: `re.IGNORECASE`)

**Returns:**

- `re.Pattern`: Compiled regex pattern

**Example:**

```python
from langops.parser.patterns.common import _p
from langops.parser.types.pipeline_types import SeverityLevel

# Create a new pattern
custom_pattern = _p(r"FATAL ERROR:")
severity = SeverityLevel.CRITICAL

# Use in pattern list
new_patterns = [(custom_pattern, severity)]
```

## Integration with Platform Patterns

Common patterns are often referenced by platform-specific patterns:

```python
# In platform-specific pattern files
PLATFORM_PATTERNS = {
    "python": "common.python",  # Reference to common patterns
    "custom": [
        (custom_pattern, SeverityLevel.ERROR)
    ]
}
```

## Performance Considerations

- **Pre-compilation**: All patterns are pre-compiled for optimal performance
- **Case Insensitive**: Patterns use `re.IGNORECASE` for consistent matching
- **Ordering**: Patterns are ordered by frequency for faster matching
- **Memory Usage**: Large pattern sets may consume significant memory

## Best Practices

### Pattern Design

1. **Specificity**: Make patterns specific enough to avoid false positives
2. **Completeness**: Cover common error scenarios for each language
3. **Severity Classification**: Use appropriate severity levels
4. **Documentation**: Document pattern purposes and examples

### Pattern Testing

```python
import re
from langops.parser.patterns.common import COMMON_PATTERNS

def test_pattern_matching(language: str, test_strings: List[str]):
    """Test pattern matching for a specific language."""
    patterns = COMMON_PATTERNS[language]
    
    for test_string in test_strings:
        matches = []
        for pattern, severity in patterns:
            if pattern.search(test_string):
                matches.append((pattern.pattern, severity))
        
        if matches:
            print(f"'{test_string}' matches: {matches}")
        else:
            print(f"'{test_string}' no matches")

# Test Python patterns
test_strings = [
    "Traceback (most recent call last):",
    "ModuleNotFoundError: No module named 'requests'",
    "This is a normal log message"
]
test_pattern_matching("python", test_strings)
```

## Extensibility

### Adding New Languages

```python
from langops.parser.patterns.common import COMMON_PATTERNS
from langops.parser.types.pipeline_types import SeverityLevel
import re

# Add patterns for a new language
COMMON_PATTERNS["rust"] = [
    (re.compile(r"error\[E\d+\]:", re.IGNORECASE), SeverityLevel.ERROR),
    (re.compile(r"thread '.+' panicked at", re.IGNORECASE), SeverityLevel.CRITICAL),
    (re.compile(r"warning:", re.IGNORECASE), SeverityLevel.WARNING),
]
```

### Pattern Validation

```python
from langops.parser.patterns.common import COMMON_PATTERNS
from langops.parser.types.pipeline_types import SeverityLevel

def validate_patterns(language: str) -> bool:
    """Validate patterns for a specific language."""
    if language not in COMMON_PATTERNS:
        return False
    
    patterns = COMMON_PATTERNS[language]
    
    for pattern, severity in patterns:
        if not hasattr(pattern, 'search'):
            return False
        if not isinstance(severity, SeverityLevel):
            return False
    
    return True
```

## Testing

The common patterns module is thoroughly tested with:

- **Pattern Matching**: Tests for accurate pattern matching across all languages
- **Severity Classification**: Tests for correct severity assignment
- **Regex Compilation**: Tests for proper pattern compilation
- **Performance**: Tests for pattern matching performance
- **Real-world Data**: Tests with actual log data from various sources
