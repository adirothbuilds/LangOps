# Parser Patterns

## Overview

The `langops.parser.patterns` module provides platform-specific and common error patterns for parsing CI/CD pipeline logs. These patterns are used to identify and classify errors, warnings, and other important events in log data.

## Modules

### [common.py](common.md)

Common error patterns shared across multiple platforms and programming languages.

### [jenkins.py](jenkins.md)

Jenkins-specific error patterns and stage detection rules.

### [github_actions.py](github_actions.md)

GitHub Actions-specific error patterns and workflow detection rules.

### [gitlab_ci.py](gitlab_ci.md)

GitLab CI-specific error patterns and pipeline detection rules.

### [azure_devops.py](azure_devops.md)

Azure DevOps-specific error patterns and build detection rules.

## Pattern Structure

All patterns follow a consistent structure:

```python
PLATFORM_PATTERNS = {
    "language_name": [
        (compiled_regex, SeverityLevel.LEVEL),
        # More patterns...
    ],
    # More languages...
}

PLATFORM_STAGE_PATTERNS = [
    compiled_regex,
    # More stage patterns...
]
```

## Usage

### Direct Pattern Access

```python
from langops.parser.patterns.jenkins import JENKINS_PATTERNS
from langops.parser.patterns.common import COMMON_PATTERNS

# Use Jenkins patterns
jenkins_python_patterns = JENKINS_PATTERNS["python"]

# Use common patterns
common_python_patterns = COMMON_PATTERNS["python"]
```

### Pattern Resolution

```python
from langops.parser.utils.resolver import PatternResolver

# Resolve patterns with common references
patterns = {
    "python": "common.python",
    "custom": [(r"ERROR:", "ERROR")]
}

resolver = PatternResolver()
resolved = resolver.resolve_patterns(patterns)
```

## Supported Platforms

### CI/CD Platforms

- **Jenkins**: Traditional CI/CD with build stages
- **GitHub Actions**: Git-based workflows with actions
- **GitLab CI**: Git-integrated continuous integration
- **Azure DevOps**: Microsoft's DevOps platform

### Programming Languages

- **Python**: Error patterns for Python applications
- **Node.js**: Error patterns for JavaScript/Node.js applications
- **Java**: Error patterns for Java applications
- **Go**: Error patterns for Go applications
- **Docker**: Error patterns for containerized applications

## Severity Levels

All patterns are classified by severity:

- **INFO**: Informational messages
- **WARNING**: Warnings that don't stop execution
- **ERROR**: Errors that may cause failure
- **CRITICAL**: Critical errors that stop execution

## Pattern Development

### Adding New Patterns

```python
from langops.parser.types.pipeline_types import SeverityLevel
import re

# Add new patterns to existing language
NEW_PATTERNS = [
    (re.compile(r"CustomError:", re.IGNORECASE), SeverityLevel.ERROR),
    (re.compile(r"CustomWarning:", re.IGNORECASE), SeverityLevel.WARNING),
]

# Extend existing patterns
JENKINS_PATTERNS["python"].extend(NEW_PATTERNS)
```

### Pattern Testing

```python
import re
from langops.parser.types.pipeline_types import SeverityLevel

def test_pattern(pattern: str, test_strings: List[str]) -> Dict[str, bool]:
    """Test a pattern against multiple strings."""
    compiled_pattern = re.compile(pattern, re.IGNORECASE)
    return {test_string: bool(compiled_pattern.search(test_string)) 
            for test_string in test_strings}

# Test a pattern
pattern = r"Error:"
test_strings = ["Error: Something went wrong", "Warning: Check this"]
results = test_pattern(pattern, test_strings)
print(results)  # {'Error: Something went wrong': True, 'Warning: Check this': False}
```

## Architecture

The patterns module is designed with:

- **Modularity**: Each platform has its own pattern module
- **Reusability**: Common patterns are shared across platforms
- **Extensibility**: Easy to add new platforms and languages
- **Performance**: Compiled regex patterns for fast matching
- **Type Safety**: Proper type annotations and enums

## Integration

### With Pipeline Parsers

```python
from langops.parser.patterns.jenkins import JENKINS_PATTERNS, JENKINS_STAGE_PATTERNS
from langops.parser.pipeline_parser import PipelineParser

# Create parser with Jenkins patterns
parser = PipelineParser(source="jenkins")
# Patterns are automatically loaded

# Parse with specific patterns
result = parser.parse(log_content, patterns=JENKINS_PATTERNS)
```

### With Pattern Resolver

```python
from langops.parser.utils.resolver import PatternResolver

# Create configuration that references patterns
config = {
    "python": "common.python",
    "jenkins": "jenkins.python",
    "custom": [(r"CUSTOM_ERROR:", "ERROR")]
}

# Resolve patterns
resolver = PatternResolver()
resolved = resolver.resolve_patterns(config)
```

## Performance Considerations

- **Compilation**: Patterns are pre-compiled for performance
- **Ordering**: Patterns are ordered by frequency for optimal matching
- **Caching**: Consider caching compiled patterns for repeated use
- **Memory Usage**: Large pattern sets may consume significant memory

## Best Practices

### Pattern Design

1. **Specificity**: Make patterns specific enough to avoid false positives
2. **Performance**: Use efficient regex constructs
3. **Maintainability**: Comment complex patterns
4. **Testing**: Test patterns with real log data

### Pattern Organization

1. **Grouping**: Group related patterns together
2. **Naming**: Use descriptive names for pattern variables
3. **Documentation**: Document pattern purposes and examples
4. **Versioning**: Version patterns when making breaking changes

## Testing

The patterns module is thoroughly tested with:

- **Pattern Matching**: Tests for accurate pattern matching
- **Severity Classification**: Tests for correct severity assignment
- **Performance**: Tests for pattern matching performance
- **Integration**: Tests with real log data from various platforms
