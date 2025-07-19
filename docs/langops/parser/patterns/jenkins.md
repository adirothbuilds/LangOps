# Jenkins Patterns

## Overview

The `jenkins.py` module provides Jenkins-specific error patterns and stage detection rules for parsing Jenkins pipeline logs. These patterns are optimized for Jenkins' unique log format and build system characteristics.

## Pattern Categories

### Groovy Patterns

Jenkins uses Groovy for pipeline scripts, so this module includes comprehensive Groovy error patterns:

```python
JENKINS_PATTERNS = {
    "groovy": [
        (groovy.lang.MissingPropertyException, SeverityLevel.ERROR),
        (unable to resolve class, SeverityLevel.ERROR),
        (groovy.lang.MissingMethodException, SeverityLevel.ERROR),
        # ... more patterns
    ]
}
```

**Groovy-Specific Patterns:**

- `groovy.lang.MissingPropertyException` - Missing property access (ERROR)
- `unable to resolve class` - Class resolution failures (ERROR)
- `groovy.lang.MissingMethodException` - Missing method calls (ERROR)
- `groovy.lang.GroovyRuntimeException` - Runtime exceptions (ERROR)
- `java.lang.ClassCastException` - Type casting errors (ERROR)
- `java.lang.NullPointerException` - Null pointer exceptions (CRITICAL)
- `No such property:` - Property access errors (ERROR)
- `WorkflowScript` - Workflow script errors (ERROR)
- `MultipleCompilationErrorsException` - Compilation errors (CRITICAL)
- `Cannot invoke method.*on null object` - Null method invocation (ERROR)

### Common Language Patterns

Jenkins patterns reference common patterns for various languages:

```python
JENKINS_PATTERNS = {
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
```

These references are automatically resolved to the corresponding patterns from the `common.py` module.

## Stage Detection Patterns

### `JENKINS_STAGE_PATTERNS`

Jenkins-specific patterns for detecting pipeline stages:

```python
JENKINS_STAGE_PATTERNS = [
    # Timestamped stage info
    re.compile(r"\[\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[.,]?\d*\]\s+\[INFO\]\s+Stage:\s+(.+)"),
    
    # Pipeline stage blocks
    re.compile(r"^\s*\[\s*Pipeline\s*\]\s*\{\s*stage\s*\(.+?\)"),
    re.compile(r"^\s*\[\s*Pipeline\s*\]\s*stage\s*\('(.+?)'\)"),
    
    # Jenkins stage runners
    re.compile(r"\[jenkins\]\s+Running stage\s+'(.+?)'"),
    re.compile(r"\[jenkins\]\s+Entering stage\s+'(.+?)'"),
    re.compile(r"\[jenkins\]\s+(.+?)"),
    
    # Echo-based stage detection
    re.compile(r"^\s*\[\s*Pipeline\s*\]\s*echo\s+.*Starting\s+stage:\s+(.+)"),
]
```

**Stage Pattern Types:**

1. **Timestamped Stages**: `[2024-01-01T12:00:00] [INFO] Stage: Build`
2. **Pipeline Blocks**: `[Pipeline] { stage('Build') }`
3. **Stage Quotes**: `[Pipeline] stage('Build')`
4. **Jenkins Runners**: `[jenkins] Running stage 'Build'`
5. **Entry Points**: `[jenkins] Entering stage 'Build'`
6. **Generic Jenkins**: `[jenkins] Build`
7. **Echo Stages**: `[Pipeline] echo Starting stage: Build`

## Usage Examples

### Direct Pattern Usage

```python
from langops.parser.patterns.jenkins import JENKINS_PATTERNS, JENKINS_STAGE_PATTERNS

# Get Jenkins patterns
jenkins_patterns = JENKINS_PATTERNS
groovy_patterns = JENKINS_PATTERNS["groovy"]

# Get stage patterns
stage_patterns = JENKINS_STAGE_PATTERNS

# Test pattern matching
import re
log_line = "groovy.lang.MissingPropertyException: No such property: invalidVar"
for pattern, severity in groovy_patterns:
    if pattern.search(log_line):
        print(f"Found {severity} error: {log_line}")
```

### With Pipeline Parser

```python
from langops.parser.pipeline_parser import PipelineParser

# Create parser with Jenkins patterns
parser = PipelineParser(source="jenkins")

# Parse Jenkins logs
jenkins_logs = """
[2024-01-01T12:00:00] [INFO] Stage: Build
[Pipeline] stage('Build')
groovy.lang.MissingPropertyException: No such property: invalidVar
[Pipeline] stage('Test')
Build completed successfully
"""

result = parser.parse(jenkins_logs)
print(f"Found {len(result.stages)} stages")
for stage in result.stages:
    print(f"Stage: {stage.name} ({len(stage.content)} logs)")
```

### Pattern Resolution

```python
from langops.parser.utils.resolver import PatternResolver

# Resolve Jenkins patterns
resolver = PatternResolver()
resolved_patterns = resolver.resolve_patterns(JENKINS_PATTERNS)

# Now resolved_patterns contains actual pattern objects instead of string references
for language, patterns in resolved_patterns.items():
    print(f"{language}: {len(patterns)} patterns")
```

## Jenkins-Specific Features

### Groovy Pipeline Support

Jenkins uses Groovy for pipeline definitions, requiring specialized error patterns:

```python
# Example Groovy errors in Jenkins logs
groovy_errors = [
    "groovy.lang.MissingPropertyException: No such property: nonExistentVar",
    "unable to resolve class NonExistentClass",
    "groovy.lang.MissingMethodException: No signature of method: java.lang.String.nonExistentMethod()",
    "Cannot invoke method toString() on null object"
]

# These are automatically detected by Jenkins patterns
```

### Stage Detection

Jenkins has multiple ways to define and log stages:

```python
# Different Jenkins stage formats
jenkins_stage_formats = [
    "[2024-01-01T12:00:00] [INFO] Stage: Build Process",
    "[Pipeline] { stage('Build Process') }",
    "[Pipeline] stage('Build Process')",
    "[jenkins] Running stage 'Build Process'",
    "[jenkins] Entering stage 'Build Process'",
    "[Pipeline] echo Starting stage: Build Process"
]

# All formats are handled by JENKINS_STAGE_PATTERNS
```

### Build System Integration

Jenkins integrates with various build systems, covered by common patterns:

```python
# Jenkins can run various build tools
build_tools = [
    "python",   # Python scripts and tests
    "nodejs",   # npm, yarn, Node.js applications
    "java",     # Maven, Gradle, Ant builds
    "dotnet",   # .NET builds and tests
    "shell",    # Shell scripts
    "batch",    # Windows batch files
    "docker",   # Docker builds
    "kubernetes", # K8s deployments
    "make"      # Make-based builds
]

# All are supported through common pattern references
```

## Integration Examples

### Custom Jenkins Parser

```python
from langops.parser.patterns.jenkins import JENKINS_PATTERNS, JENKINS_STAGE_PATTERNS
from langops.parser.base_parser import BaseParser

class CustomJenkinsParser(BaseParser):
    def __init__(self):
        super().__init__()
        self.patterns = JENKINS_PATTERNS
        self.stage_patterns = JENKINS_STAGE_PATTERNS
    
    def parse_jenkins_build(self, log_content: str):
        """Parse Jenkins build logs with custom logic."""
        # Custom parsing logic using Jenkins patterns
        stages = self._detect_stages(log_content)
        errors = self._detect_errors(log_content)
        return {"stages": stages, "errors": errors}
```

### Jenkins Log Analysis

```python
from langops.parser.patterns.jenkins import JENKINS_PATTERNS
from langops.parser.types.pipeline_types import SeverityLevel

def analyze_jenkins_build(log_content: str) -> Dict[str, Any]:
    """Analyze Jenkins build logs for issues."""
    analysis = {
        "total_lines": len(log_content.splitlines()),
        "errors_by_language": {},
        "severity_counts": {level.value: 0 for level in SeverityLevel}
    }
    
    # Analyze each language's patterns
    for language, patterns in JENKINS_PATTERNS.items():
        if isinstance(patterns, str):
            continue  # Skip common pattern references
        
        error_count = 0
        for pattern, severity in patterns:
            matches = pattern.findall(log_content)
            error_count += len(matches)
            analysis["severity_counts"][severity.value] += len(matches)
        
        analysis["errors_by_language"][language] = error_count
    
    return analysis
```

### Jenkins Stage Extraction

```python
from langops.parser.patterns.jenkins import JENKINS_STAGE_PATTERNS
import re

def extract_jenkins_stages(log_content: str) -> List[Dict[str, Any]]:
    """Extract stages from Jenkins logs."""
    stages = []
    lines = log_content.splitlines()
    
    for i, line in enumerate(lines):
        for pattern in JENKINS_STAGE_PATTERNS:
            match = pattern.search(line)
            if match:
                stage_name = match.group(1) if match.groups() else "Unknown"
                stages.append({
                    "name": stage_name,
                    "line": i + 1,
                    "raw_line": line.strip()
                })
                break
    
    return stages
```

## Performance Considerations

### Pattern Optimization

- **Pre-compiled Patterns**: All patterns are pre-compiled for optimal performance
- **Ordered Matching**: Patterns are ordered by frequency for faster matching
- **Lazy Evaluation**: Common patterns are resolved only when needed

### Memory Usage

```python
# Efficient pattern usage
from langops.parser.patterns.jenkins import JENKINS_PATTERNS

# Get only needed patterns
groovy_patterns = JENKINS_PATTERNS["groovy"]
# Instead of loading all patterns unnecessarily

# Use specific patterns for targeted matching
def check_groovy_errors(log_line: str) -> bool:
    """Check for Groovy errors efficiently."""
    return any(pattern.search(log_line) for pattern, _ in groovy_patterns)
```

## Testing and Validation

### Pattern Testing

```python
from langops.parser.patterns.jenkins import JENKINS_PATTERNS

def test_jenkins_patterns():
    """Test Jenkins patterns with sample data."""
    test_cases = [
        ("groovy.lang.MissingPropertyException: No such property: test", "groovy", True),
        ("unable to resolve class TestClass", "groovy", True),
        ("This is a normal log message", "groovy", False),
    ]
    
    groovy_patterns = JENKINS_PATTERNS["groovy"]
    
    for test_input, language, expected in test_cases:
        found = any(pattern.search(test_input) for pattern, _ in groovy_patterns)
        assert found == expected, f"Pattern test failed for: {test_input}"
    
    print("All Jenkins pattern tests passed!")

# Run tests
test_jenkins_patterns()
```

### Stage Pattern Testing

```python
from langops.parser.patterns.jenkins import JENKINS_STAGE_PATTERNS

def test_stage_patterns():
    """Test Jenkins stage patterns."""
    test_stages = [
        "[2024-01-01T12:00:00] [INFO] Stage: Build Process",
        "[Pipeline] stage('Test Suite')",
        "[jenkins] Running stage 'Deploy'",
        "[Pipeline] echo Starting stage: Cleanup"
    ]
    
    for stage_line in test_stages:
        matched = any(pattern.search(stage_line) for pattern in JENKINS_STAGE_PATTERNS)
        assert matched, f"Stage pattern test failed for: {stage_line}"
    
    print("All Jenkins stage pattern tests passed!")

# Run tests
test_stage_patterns()
```

## Best Practices

### Pattern Usage

1. **Specificity**: Use specific patterns for Jenkins-unique formats
2. **Fallback**: Rely on common patterns for standard languages
3. **Performance**: Cache resolved patterns for repeated use
4. **Validation**: Always test patterns with real Jenkins logs

### Integration

1. **Parser Integration**: Use with PipelineParser for full functionality
2. **Custom Logic**: Extend patterns for specific Jenkins configurations
3. **Error Handling**: Handle pattern resolution errors gracefully
4. **Documentation**: Document custom patterns and their purposes

## Extension Points

### Adding Custom Patterns

```python
from langops.parser.patterns.jenkins import JENKINS_PATTERNS
from langops.parser.types.pipeline_types import SeverityLevel
import re

# Add custom Jenkins patterns
JENKINS_PATTERNS["custom"] = [
    (re.compile(r"CUSTOM_JENKINS_ERROR:", re.IGNORECASE), SeverityLevel.ERROR),
    (re.compile(r"CUSTOM_JENKINS_WARNING:", re.IGNORECASE), SeverityLevel.WARNING),
]

# Add custom stage patterns
from langops.parser.patterns.jenkins import JENKINS_STAGE_PATTERNS
JENKINS_STAGE_PATTERNS.append(
    re.compile(r"CUSTOM:\s+Stage\s+(.+)", re.IGNORECASE)
)
```

### Jenkins Plugin Support

```python
# Support for specific Jenkins plugins
JENKINS_PLUGIN_PATTERNS = {
    "maven": [
        (re.compile(r"\[ERROR\].*BUILD FAILURE", re.IGNORECASE), SeverityLevel.CRITICAL),
        (re.compile(r"\[WARNING\]", re.IGNORECASE), SeverityLevel.WARNING),
    ],
    "gradle": [
        (re.compile(r"BUILD FAILED", re.IGNORECASE), SeverityLevel.CRITICAL),
        (re.compile(r"Task.*FAILED", re.IGNORECASE), SeverityLevel.ERROR),
    ]
}

# Extend Jenkins patterns
JENKINS_PATTERNS.update(JENKINS_PLUGIN_PATTERNS)
```

## Testing

The Jenkins patterns module is thoroughly tested with:

- **Pattern Matching**: Tests with real Jenkins logs
- **Stage Detection**: Tests for various Jenkins stage formats
- **Groovy Errors**: Comprehensive tests for Groovy-specific errors
- **Integration**: Tests with PipelineParser and other components
- **Performance**: Tests for pattern matching efficiency
