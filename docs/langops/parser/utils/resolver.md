# Pattern Resolver

## Overview

The `resolver.py` module provides the `PatternResolver` class for resolving and loading patterns for different platforms and programming languages. It enables dynamic pattern loading from configuration files and resolution of common pattern references.

## Classes

### `PatternResolver`

A helper class for resolving and loading patterns for different platforms and languages.

## Static Methods

### `resolve_patterns(platform_dict: Dict[str, Any]) -> Dict[str, List]`

Resolves patterns for different languages based on the provided platform dictionary.

**Parameters:**

- `platform_dict` (Dict[str, Any]): A dictionary where keys are language names and values are either:
  - A list of tuples `(regex, severity)`
  - A string indicating a common pattern (e.g., `"common.python"`)

**Returns:**

- `Dict[str, List]`: A dictionary with resolved patterns for each language

**Raises:**

- `KeyError`: If a referenced common pattern key is missing
- `Exception`: For any unexpected errors during resolution

**Example:**

```python
from langops.parser.utils.resolver import PatternResolver

# Define platform patterns with common references
platform_patterns = {
    "python": "common.python",  # Reference to common patterns
    "custom": [
        (r"CUSTOM_ERROR:", "ERROR"),
        (r"CUSTOM_WARNING:", "WARNING")
    ]
}

# Resolve patterns
resolver = PatternResolver()
resolved = resolver.resolve_patterns(platform_patterns)

print(resolved)
# {
#     'python': [(compiled_regex, SeverityLevel.ERROR), ...],
#     'custom': [(compiled_regex, SeverityLevel.ERROR), ...]
# }
```

### `load_patterns(config_file: str) -> Dict[str, Any]`

Loads custom patterns from a YAML configuration file.

**Parameters:**

- `config_file` (str): Path to the YAML configuration file containing custom patterns

**Returns:**

- `Dict[str, Any]`: A dictionary with resolved patterns and configuration

**Return Structure:**

```python
{
    "source": str,  # The source platform name
    "patterns": Dict[str, List],  # Language-specific patterns
    "stage_patterns": List[re.Pattern]  # Compiled stage detection patterns
}
```

**Raises:**

- `FileNotFoundError`: If the configuration file is not found
- `yaml.YAMLError`: If there is an error parsing the YAML file
- `KeyError`: If the YAML structure is missing required keys
- `Exception`: For any unexpected errors during loading

**Example:**

```python
from langops.parser.utils.resolver import PatternResolver

# Load patterns from YAML file
resolver = PatternResolver()
config = resolver.load_patterns("custom_patterns.yaml")

print(config["source"])  # "custom_platform"
print(config["patterns"])  # Resolved language patterns
print(config["stage_patterns"])  # Compiled stage patterns
```

## YAML Configuration Format

The configuration file should follow this structure:

```yaml
source: "custom_platform"
patterns:
  python:
    - regex: "CustomError:"
      severity: "ERROR"
    - regex: "CustomWarning:"
      severity: "WARNING"
  javascript:
    - regex: "TypeError:"
      severity: "ERROR"
    - regex: "DeprecationWarning:"
      severity: "WARNING"
stage_patterns:
  - "^Stage: (.+)$"
  - "^Running (.+)$"
  - "^\\[(.+)\\]$"
```

## Usage Examples

### Basic Pattern Resolution

```python
from langops.parser.utils.resolver import PatternResolver

# Simple pattern resolution
patterns = {
    "python": "common.python",
    "java": "common.java",
    "custom": [
        (r"FATAL:", "CRITICAL"),
        (r"WARN:", "WARNING")
    ]
}

resolver = PatternResolver()
resolved = resolver.resolve_patterns(patterns)

# Use resolved patterns
for language, pattern_list in resolved.items():
    print(f"{language}: {len(pattern_list)} patterns")
```

### Loading from Configuration File

```python
from langops.parser.utils.resolver import PatternResolver

# Load configuration
resolver = PatternResolver()
try:
    config = resolver.load_patterns("pipeline_patterns.yaml")
    
    # Access loaded patterns
    source = config["source"]
    patterns = config["patterns"]
    stage_patterns = config["stage_patterns"]
    
    print(f"Loaded {len(patterns)} language patterns for {source}")
    print(f"Loaded {len(stage_patterns)} stage patterns")
    
except FileNotFoundError:
    print("Configuration file not found")
except yaml.YAMLError as e:
    print(f"YAML parsing error: {e}")
```

### Creating a Custom Parser

```python
from langops.parser.utils.resolver import PatternResolver
from langops.parser.types.pipeline_types import SeverityLevel

class CustomParser:
    def __init__(self, config_file: str):
        resolver = PatternResolver()
        config = resolver.load_patterns(config_file)
        
        self.source = config["source"]
        self.patterns = config["patterns"]
        self.stage_patterns = config["stage_patterns"]
    
    def parse(self, log_content: str):
        # Use loaded patterns for parsing
        pass
```

## Integration with Common Patterns

The resolver integrates with the `COMMON_PATTERNS` dictionary from `langops.parser.patterns.common`:

```python
from langops.parser.patterns.common import COMMON_PATTERNS

# Common patterns are automatically resolved
platform_dict = {
    "python": "common.python",  # Resolves to COMMON_PATTERNS["python"]
    "nodejs": "common.nodejs"   # Resolves to COMMON_PATTERNS["nodejs"]
}
```

## Error Handling

### Pattern Resolution Errors

```python
from langops.parser.utils.resolver import PatternResolver

try:
    patterns = {"python": "common.nonexistent"}
    resolver = PatternResolver()
    resolved = resolver.resolve_patterns(patterns)
except KeyError as e:
    print(f"Missing common pattern: {e}")
```

### Configuration Loading Errors

```python
from langops.parser.utils.resolver import PatternResolver
import yaml

try:
    resolver = PatternResolver()
    config = resolver.load_patterns("invalid.yaml")
except FileNotFoundError:
    print("Configuration file not found")
except yaml.YAMLError as e:
    print(f"YAML parsing error: {e}")
except KeyError as e:
    print(f"Missing required key: {e}")
```

## Performance Considerations

- **Pattern Compilation**: Patterns are compiled once during resolution for optimal performance
- **Cache Considerations**: Consider caching resolved patterns for frequently used configurations
- **Memory Usage**: Large pattern sets may consume significant memory
- **File I/O**: Loading patterns from files involves disk I/O; consider loading once and reusing

## Extensibility

### Adding New Common Patterns

To add support for new common patterns, extend the `COMMON_PATTERNS` dictionary:

```python
# In langops.parser.patterns.common
COMMON_PATTERNS["ruby"] = [
    (re.compile(r"RuntimeError:", re.IGNORECASE), SeverityLevel.ERROR),
    (re.compile(r"NoMethodError:", re.IGNORECASE), SeverityLevel.ERROR),
]
```

### Custom Pattern Validation

```python
from langops.parser.utils.resolver import PatternResolver

class ValidatingPatternResolver(PatternResolver):
    @staticmethod
    def validate_patterns(patterns: Dict[str, Any]) -> bool:
        """Validate pattern structure before resolution."""
        for language, pattern_list in patterns.items():
            if isinstance(pattern_list, list):
                for pattern in pattern_list:
                    if not isinstance(pattern, tuple) or len(pattern) != 2:
                        return False
        return True
```

## Testing

The resolver module is thoroughly tested with 100% code coverage:

- **Pattern Resolution**: Tests for common pattern references and custom patterns
- **Configuration Loading**: Tests for valid and invalid YAML configurations
- **Error Handling**: Tests for file not found, parsing errors, and missing keys
- **Edge Cases**: Tests for empty patterns, malformed data, and boundary conditions
