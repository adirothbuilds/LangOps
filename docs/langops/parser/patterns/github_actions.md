# GitHub Actions Patterns

## Overview

The `github_actions.py` module provides GitHub Actions-specific error patterns and workflow detection rules for parsing GitHub Actions logs. These patterns are optimized for GitHub's workflow output format and action-based build system.

## Pattern Structure

### `GITHUB_ACTIONS_PATTERNS`

A dictionary containing language-specific error patterns for GitHub Actions workflows:

```python
GITHUB_ACTIONS_PATTERNS = {
    "python": "common.python",   # Reference to common Python patterns
    "nodejs": "common.nodejs",   # Reference to common Node.js patterns
    "java": "common.java",       # Reference to common Java patterns
    # ... more language references
}
```

### `GITHUB_ACTIONS_STAGE_PATTERNS`

A list of compiled regex patterns for detecting GitHub Actions workflow steps and jobs:

```python
GITHUB_ACTIONS_STAGE_PATTERNS = [
    re.compile(r"\[github\]\s+job\s+'(.+?)'", re.IGNORECASE),
    re.compile(r"::group::\s*(.+)", re.IGNORECASE),
    # ... more stage patterns
]
```

## Language Support

GitHub Actions patterns reference common patterns for standard languages:

- `"python": "common.python"` - Python error patterns
- `"nodejs": "common.nodejs"` - Node.js and TypeScript error patterns
- `"java": "common.java"` - Java and Maven error patterns
- `"dotnet": "common.dotnet"` - .NET and C# error patterns
- `"shell": "common.shell"` - Shell script error patterns
- `"batch": "common.batch"` - Windows batch script error patterns
- `"docker": "common.docker"` - Docker build and run error patterns
- `"kubernetes": "common.kubernetes"` - Kubernetes deployment error patterns
- `"make": "common.make"` - Make and build system error patterns

## Stage Detection Patterns

GitHub Actions stage patterns identify different phases of workflow execution:

### Pattern Types

1. **Job Patterns**: `\[github\]\s+job\s+'(.+?)'`
   - Matches: `[github] job 'build'`
   - Captures: `build`

2. **Step Patterns**: `\[github\]\s+step\s+'(.+?)'`
   - Matches: `[github] step 'Run tests'`
   - Captures: `Run tests`

3. **Run Patterns**: `\[github\]\s+run\s+'(.+?)'`
   - Matches: `[github] run 'npm install'`
   - Captures: `npm install`

4. **Running Patterns**: `\[github\]\s+Running\s+(?:job|step)\s+'(.+?)'`
   - Matches: `[github] Running job 'build'`
   - Captures: `build`

5. **Group Patterns**: `::group::\s*(.+)`
   - Matches: `::group::Installing dependencies`
   - Captures: `Installing dependencies`

6. **Action Patterns**: `##\[[a-z]+\]\s*Starting:\s*(.+)`
   - Matches: `##[info] Starting: Build application`
   - Captures: `Build application`

7. **Timestamped Patterns**: `\[\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[.,]?\d*\]\s+\[INFO\]\s+Stage:\s+(.+)`
   - Matches: `[2024-01-01T12:00:00] [INFO] Stage: Deploy`
   - Captures: `Deploy`

## Usage Examples

### Basic Pattern Matching

```python
from langops.parser.patterns.github_actions import GITHUB_ACTIONS_PATTERNS
from langops.parser.utils.resolver import PatternResolver

# Resolve GitHub Actions patterns
resolver = PatternResolver()
patterns = resolver.resolve_patterns(GITHUB_ACTIONS_PATTERNS)

# Check for errors in a log line
def check_github_actions_errors(log_line: str) -> List[tuple]:
    """Check for GitHub Actions-specific errors."""
    errors = []
    
    for language, language_patterns in patterns.items():
        for pattern, severity in language_patterns:
            if pattern.search(log_line):
                errors.append((language, severity, log_line))
    
    return errors

# Example usage
log_line = "Error: Cannot find module 'react'"
errors = check_github_actions_errors(log_line)
print(errors)  # [('nodejs', SeverityLevel.ERROR, "Error: Cannot find module 'react'")]
```

### Workflow Step Extraction

```python
from langops.parser.patterns.github_actions import GITHUB_ACTIONS_STAGE_PATTERNS

def extract_github_actions_steps(log_content: str) -> List[Dict[str, Any]]:
    """Extract workflow steps from GitHub Actions logs."""
    steps = []
    lines = log_content.split('\n')
    
    for line_num, line in enumerate(lines, 1):
        for pattern in GITHUB_ACTIONS_STAGE_PATTERNS:
            match = pattern.search(line)
            if match and match.groups():
                steps.append({
                    'name': match.group(1),
                    'line': line_num,
                    'pattern': pattern.pattern
                })
                break
    
    return steps

# Extract steps
log_content = """
[github] job 'build'
::group::Installing dependencies
[github] step 'Run tests'
##[info] Starting: Deploy to production
"""
steps = extract_github_actions_steps(log_content)
print(steps)
# [
#     {'name': 'build', 'line': 1, 'pattern': '...'},
#     {'name': 'Installing dependencies', 'line': 2, 'pattern': '...'},
#     {'name': 'Run tests', 'line': 3, 'pattern': '...'},
#     {'name': 'Deploy to production', 'line': 4, 'pattern': '...'}
# ]
```

### Integration with Pipeline Parser

```python
from langops.parser.patterns.github_actions import GITHUB_ACTIONS_PATTERNS, GITHUB_ACTIONS_STAGE_PATTERNS
from langops.parser.utils.resolver import PatternResolver

class GitHubActionsParser:
    """GitHub Actions-specific pipeline parser."""
    
    def __init__(self):
        self.resolver = PatternResolver()
        self.patterns = self.resolver.resolve_patterns(GITHUB_ACTIONS_PATTERNS)
        self.stage_patterns = GITHUB_ACTIONS_STAGE_PATTERNS
    
    def parse(self, log_content: str) -> Dict[str, Any]:
        """Parse GitHub Actions logs."""
        steps = self._extract_steps(log_content)
        errors = self._extract_errors(log_content)
        
        return {
            'source': 'github_actions',
            'steps': steps,
            'errors': errors,
            'metadata': self._extract_metadata(log_content)
        }
    
    def _extract_steps(self, content: str) -> List[str]:
        """Extract workflow step names."""
        steps = []
        for line in content.split('\n'):
            for pattern in self.stage_patterns:
                match = pattern.search(line)
                if match and match.groups():
                    steps.append(match.group(1))
                    break
        return steps
    
    def _extract_errors(self, content: str) -> List[Dict[str, Any]]:
        """Extract errors using resolved patterns."""
        errors = []
        for line_num, line in enumerate(content.split('\n'), 1):
            for language, patterns in self.patterns.items():
                for pattern, severity in patterns:
                    if pattern.search(line):
                        errors.append({
                            'line': line_num,
                            'language': language,
                            'severity': severity,
                            'message': line.strip()
                        })
        return errors
    
    def _extract_metadata(self, content: str) -> Dict[str, Any]:
        """Extract GitHub Actions metadata."""
        metadata = {}
        
        # Extract workflow information
        workflow_match = re.search(r"workflow:\s+(.+)", content)
        if workflow_match:
            metadata['workflow'] = workflow_match.group(1)
        
        # Extract job information
        job_match = re.search(r"job:\s+(.+)", content)
        if job_match:
            metadata['job'] = job_match.group(1)
        
        # Extract runner information
        runner_match = re.search(r"runner:\s+(.+)", content)
        if runner_match:
            metadata['runner'] = runner_match.group(1)
        
        return metadata
```

## GitHub Actions-Specific Considerations

### Workflow Structure

GitHub Actions workflows have a specific structure:

```yaml
name: CI
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Node.js
        uses: actions/setup-node@v2
      - name: Install dependencies
        run: npm install
      - name: Run tests
        run: npm test
```

### Output Format

GitHub Actions outputs logs in a specific format:

```text
##[group]Installing dependencies
##[info] Starting: npm install
##[command]/usr/bin/npm install
##[endgroup]
```

### Action Annotations

GitHub Actions uses special annotations:

- `::group::` - Creates collapsible log groups
- `##[info]` - Information messages
- `##[warning]` - Warning messages
- `##[error]` - Error messages
- `##[debug]` - Debug messages

### Step Detection

GitHub Actions steps can be detected through:

- **Job Names**: `[github] job 'build'`
- **Step Names**: `[github] step 'Run tests'`
- **Run Commands**: `[github] run 'npm install'`
- **Group Markers**: `::group::Installing dependencies`
- **Action Markers**: `##[info] Starting: Build`

## Performance Considerations

- **Pattern Compilation**: All patterns are pre-compiled for performance
- **Common Patterns**: Leverages shared common patterns for efficiency
- **Memory Usage**: Minimal memory footprint due to pattern references
- **Step Extraction**: Efficient step boundary detection

## Best Practices

### Pattern Usage

1. **Action Focus**: Understand GitHub Actions-specific output format
2. **Step Boundaries**: Use step patterns to segment workflow analysis
3. **Error Context**: Include action context for better error understanding
4. **Performance**: Cache resolved patterns for repeated workflows

### Error Handling

```python
from langops.parser.patterns.github_actions import GITHUB_ACTIONS_PATTERNS
from langops.parser.utils.resolver import PatternResolver

def safe_github_actions_parsing(log_content: str) -> Dict[str, Any]:
    """Safely parse GitHub Actions logs with error handling."""
    try:
        resolver = PatternResolver()
        patterns = resolver.resolve_patterns(GITHUB_ACTIONS_PATTERNS)
        
        # Parse with error handling
        return parse_github_actions_logs(log_content, patterns)
    except Exception as e:
        return {
            'error': str(e),
            'source': 'github_actions',
            'steps': [],
            'errors': []
        }
```

## Extensibility

### Adding Custom Patterns

```python
from langops.parser.patterns.github_actions import GITHUB_ACTIONS_PATTERNS, GITHUB_ACTIONS_STAGE_PATTERNS
from langops.parser.types.pipeline_types import SeverityLevel
import re

# Add custom GitHub Actions patterns
GITHUB_ACTIONS_PATTERNS["custom"] = [
    (re.compile(r"CUSTOM_ACTION_ERROR:", re.IGNORECASE), SeverityLevel.ERROR),
    (re.compile(r"CUSTOM_ACTION_WARNING:", re.IGNORECASE), SeverityLevel.WARNING),
]

# Add custom step patterns
GITHUB_ACTIONS_STAGE_PATTERNS.extend([
    re.compile(r"CUSTOM_STEP:\s+(.+)", re.IGNORECASE),
])
```

### Action-Specific Patterns

```python
# Add patterns for specific GitHub Actions
GITHUB_ACTIONS_PATTERNS["jest"] = [
    (re.compile(r"Tests:\s+\d+ failed", re.IGNORECASE), SeverityLevel.ERROR),
    (re.compile(r"Snapshots:\s+\d+ failed", re.IGNORECASE), SeverityLevel.ERROR),
]

GITHUB_ACTIONS_PATTERNS["eslint"] = [
    (re.compile(r"✖ \d+ problems?", re.IGNORECASE), SeverityLevel.ERROR),
    (re.compile(r"\d+ errors?", re.IGNORECASE), SeverityLevel.ERROR),
]
```

## Testing

The GitHub Actions patterns module is thoroughly tested with:

- **Pattern Matching**: Tests for accurate error detection across all supported languages
- **Step Detection**: Tests for various GitHub Actions workflow formats
- **Integration**: Tests with real GitHub Actions log data
- **Performance**: Tests for pattern matching efficiency
- **Edge Cases**: Tests for malformed logs and boundary conditions
