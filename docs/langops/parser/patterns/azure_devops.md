# Azure DevOps Patterns

## Overview

The `azure_devops.py` module provides Azure DevOps-specific error patterns and pipeline detection rules for parsing Azure DevOps logs. These patterns are optimized for Azure DevOps' pipeline output format and task-based build system.

## Pattern Structure

### `AZURE_DEVOPS_PATTERNS`

A dictionary containing language-specific error patterns for Azure DevOps pipelines:

```python
AZURE_DEVOPS_PATTERNS = {
    "python": "common.python",   # Reference to common Python patterns
    "nodejs": "common.nodejs",   # Reference to common Node.js patterns
    "java": "common.java",       # Reference to common Java patterns
    # ... more language references
}
```

### `AZURE_DEVOPS_STAGE_PATTERNS`

A list of compiled regex patterns for detecting Azure DevOps pipeline stages, steps, and tasks:

```python
AZURE_DEVOPS_STAGE_PATTERNS = [
    re.compile(r"^##\[group\]Starting: (.+)", re.IGNORECASE),
    re.compile(r"^##\[section\]Starting: (.+)", re.IGNORECASE),
    # ... more stage patterns
]
```

## Language Support

Azure DevOps patterns reference common patterns for standard languages:

- `"python": "common.python"` - Python error patterns
- `"nodejs": "common.nodejs"` - Node.js and npm error patterns
- `"java": "common.java"` - Java and Maven error patterns
- `"dotnet": "common.dotnet"` - .NET and C# error patterns
- `"shell": "common.shell"` - Shell script error patterns
- `"batch": "common.batch"` - Windows batch script error patterns
- `"docker": "common.docker"` - Docker build and run error patterns
- `"kubernetes": "common.kubernetes"` - Kubernetes deployment error patterns
- `"make": "common.make"` - Make and build system error patterns

## Stage Detection Patterns

Azure DevOps stage patterns identify different phases of pipeline execution:

### Pattern Types

1. **Group Patterns**: `^##\[group\]Starting: (.+)`
   - Matches: `##[group]Starting: Build Solution`
   - Captures: `Build Solution`

2. **Section Patterns**: `^##\[section\]Starting: (.+)`
   - Matches: `##[section]Starting: Run Tests`
   - Captures: `Run Tests`

3. **Stage Patterns**: `^##\[stage\]Starting: (.+)`
   - Matches: `##[stage]Starting: Deploy`
   - Captures: `Deploy`

4. **Step Patterns**: `^##\[step\]Starting: (.+)`
   - Matches: `##[step]Starting: Publish Test Results`
   - Captures: `Publish Test Results`

5. **Task Patterns**: `^##\[task\] (.+)`
   - Matches: `##[task] MSBuild@1`
   - Captures: `MSBuild@1`

6. **Command Patterns**: `^\[command\] (.+)`
   - Matches: `[command] dotnet build`
   - Captures: `dotnet build`

7. **Generic Starting Patterns**: `^Starting: (.+)`
   - Matches: `Starting: Build application`
   - Captures: `Build application`

## Usage Examples

### Basic Pattern Matching

```python
from langops.parser.patterns.azure_devops import AZURE_DEVOPS_PATTERNS
from langops.parser.utils.resolver import PatternResolver

# Resolve Azure DevOps patterns
resolver = PatternResolver()
patterns = resolver.resolve_patterns(AZURE_DEVOPS_PATTERNS)

# Check for errors in a log line
def check_azure_devops_errors(log_line: str) -> List[tuple]:
    """Check for Azure DevOps-specific errors."""
    errors = []
    
    for language, language_patterns in patterns.items():
        for pattern, severity in language_patterns:
            if pattern.search(log_line):
                errors.append((language, severity, log_line))
    
    return errors

# Example usage
log_line = "MSBuild error CS1234: The type or namespace name 'InvalidType' could not be found"
errors = check_azure_devops_errors(log_line)
print(errors)  # [('dotnet', SeverityLevel.ERROR, "MSBuild error CS1234...")]
```

### Pipeline Stage Extraction

```python
from langops.parser.patterns.azure_devops import AZURE_DEVOPS_STAGE_PATTERNS

def extract_azure_devops_stages(log_content: str) -> List[Dict[str, Any]]:
    """Extract pipeline stages from Azure DevOps logs."""
    stages = []
    lines = log_content.split('\n')
    
    for line_num, line in enumerate(lines, 1):
        for pattern in AZURE_DEVOPS_STAGE_PATTERNS:
            match = pattern.search(line)
            if match and match.groups():
                stages.append({
                    'name': match.group(1),
                    'line': line_num,
                    'pattern': pattern.pattern,
                    'type': _get_stage_type(pattern.pattern)
                })
                break
    
    return stages

def _get_stage_type(pattern: str) -> str:
    """Determine stage type from pattern."""
    if 'group' in pattern:
        return 'group'
    elif 'section' in pattern:
        return 'section'
    elif 'stage' in pattern:
        return 'stage'
    elif 'step' in pattern:
        return 'step'
    elif 'task' in pattern:
        return 'task'
    elif 'command' in pattern:
        return 'command'
    else:
        return 'generic'

# Extract stages
log_content = """
##[group]Starting: Build Solution
##[section]Starting: Run Tests
##[stage]Starting: Deploy
##[step]Starting: Publish Test Results
##[task] MSBuild@1
[command] dotnet build
Starting: Cleanup
"""
stages = extract_azure_devops_stages(log_content)
print(stages)
# [
#     {'name': 'Build Solution', 'line': 1, 'pattern': '...', 'type': 'group'},
#     {'name': 'Run Tests', 'line': 2, 'pattern': '...', 'type': 'section'},
#     # ... more stages
# ]
```

### Integration with Pipeline Parser

```python
from langops.parser.patterns.azure_devops import AZURE_DEVOPS_PATTERNS, AZURE_DEVOPS_STAGE_PATTERNS
from langops.parser.utils.resolver import PatternResolver

class AzureDevOpsParser:
    """Azure DevOps-specific pipeline parser."""
    
    def __init__(self):
        self.resolver = PatternResolver()
        self.patterns = self.resolver.resolve_patterns(AZURE_DEVOPS_PATTERNS)
        self.stage_patterns = AZURE_DEVOPS_STAGE_PATTERNS
    
    def parse(self, log_content: str) -> Dict[str, Any]:
        """Parse Azure DevOps logs."""
        stages = self._extract_stages(log_content)
        errors = self._extract_errors(log_content)
        
        return {
            'source': 'azure_devops',
            'stages': stages,
            'errors': errors,
            'metadata': self._extract_metadata(log_content)
        }
    
    def _extract_stages(self, content: str) -> List[Dict[str, Any]]:
        """Extract pipeline stage information."""
        stages = []
        for line_num, line in enumerate(content.split('\n'), 1):
            for pattern in self.stage_patterns:
                match = pattern.search(line)
                if match and match.groups():
                    stages.append({
                        'name': match.group(1),
                        'line': line_num,
                        'type': self._get_stage_type(pattern.pattern)
                    })
                    break
        return stages
    
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
        """Extract Azure DevOps metadata."""
        metadata = {}
        
        # Extract pipeline information
        pipeline_match = re.search(r"Pipeline: (.+)", content)
        if pipeline_match:
            metadata['pipeline'] = pipeline_match.group(1)
        
        # Extract agent information
        agent_match = re.search(r"Agent: (.+)", content)
        if agent_match:
            metadata['agent'] = agent_match.group(1)
        
        # Extract job information
        job_match = re.search(r"Job: (.+)", content)
        if job_match:
            metadata['job'] = job_match.group(1)
        
        return metadata
    
    def _get_stage_type(self, pattern: str) -> str:
        """Determine stage type from pattern."""
        if 'group' in pattern:
            return 'group'
        elif 'section' in pattern:
            return 'section'
        elif 'stage' in pattern:
            return 'stage'
        elif 'step' in pattern:
            return 'step'
        elif 'task' in pattern:
            return 'task'
        elif 'command' in pattern:
            return 'command'
        else:
            return 'generic'
```

## Azure DevOps-Specific Considerations

### Pipeline Structure

Azure DevOps pipelines are defined in `azure-pipelines.yml`:

```yaml
trigger:
- main

pool:
  vmImage: 'ubuntu-latest'

stages:
- stage: Build
  displayName: Build stage
  jobs:
  - job: Build
    displayName: Build job
    steps:
    - task: DotNetCoreCLI@2
      displayName: 'Build project'
      inputs:
        command: 'build'
```

### Output Format

Azure DevOps outputs logs in a specific format:

```text
##[group]Starting: Build Solution
##[command]dotnet build MyProject.sln
##[section]Starting: Run Tests
##[command]dotnet test MyProject.Tests.dll
##[task] PublishTestResults@2
##[section]Finishing: Run Tests
##[group]Finishing: Build Solution
```

### Log Annotations

Azure DevOps uses specific annotations for different log types:

- `##[group]` - Collapsible log groups
- `##[section]` - Pipeline sections
- `##[stage]` - Pipeline stages
- `##[step]` - Individual steps
- `##[task]` - Specific tasks
- `##[command]` - Command execution
- `##[error]` - Error messages
- `##[warning]` - Warning messages
- `##[debug]` - Debug information

### Stage Types

Azure DevOps has different types of execution units:

1. **Stages**: Top-level execution units
2. **Jobs**: Execution units within stages
3. **Steps**: Individual tasks within jobs
4. **Tasks**: Specific operations (built-in or custom)
5. **Commands**: Shell commands or scripts

### Stage Detection

Azure DevOps stages can be detected through:

- **Group Markers**: `##[group]Starting: Build Solution`
- **Section Markers**: `##[section]Starting: Run Tests`
- **Stage Markers**: `##[stage]Starting: Deploy`
- **Step Markers**: `##[step]Starting: Publish Results`
- **Task Markers**: `##[task] MSBuild@1`
- **Command Markers**: `[command] dotnet build`

## Performance Considerations

- **Pattern Compilation**: All patterns are pre-compiled for performance
- **Common Patterns**: Leverages shared common patterns for efficiency
- **Memory Usage**: Minimal memory footprint due to pattern references
- **Stage Hierarchy**: Efficient handling of nested stage structures

## Best Practices

### Pattern Usage

1. **Annotation Awareness**: Use Azure DevOps annotations for accurate parsing
2. **Stage Hierarchy**: Understand the relationship between stages, jobs, and steps
3. **Task Context**: Include task and command context for better error understanding
4. **Performance**: Cache resolved patterns for repeated pipeline runs

### Error Handling

```python
from langops.parser.patterns.azure_devops import AZURE_DEVOPS_PATTERNS
from langops.parser.utils.resolver import PatternResolver

def safe_azure_devops_parsing(log_content: str) -> Dict[str, Any]:
    """Safely parse Azure DevOps logs with error handling."""
    try:
        resolver = PatternResolver()
        patterns = resolver.resolve_patterns(AZURE_DEVOPS_PATTERNS)
        
        # Parse with error handling
        return parse_azure_devops_logs(log_content, patterns)
    except Exception as e:
        return {
            'error': str(e),
            'source': 'azure_devops',
            'stages': [],
            'errors': []
        }
```

## Extensibility

### Adding Custom Patterns

```python
from langops.parser.patterns.azure_devops import AZURE_DEVOPS_PATTERNS, AZURE_DEVOPS_STAGE_PATTERNS
from langops.parser.types.pipeline_types import SeverityLevel
import re

# Add custom Azure DevOps patterns
AZURE_DEVOPS_PATTERNS["custom"] = [
    (re.compile(r"##\[error\]CUSTOM_ERROR:", re.IGNORECASE), SeverityLevel.ERROR),
    (re.compile(r"##\[warning\]CUSTOM_WARNING:", re.IGNORECASE), SeverityLevel.WARNING),
]

# Add custom stage patterns
AZURE_DEVOPS_STAGE_PATTERNS.extend([
    re.compile(r"##\[custom\]Starting: (.+)", re.IGNORECASE),
])
```

### Task-Specific Patterns

```python
# Add patterns for specific Azure DevOps tasks
AZURE_DEVOPS_PATTERNS["msbuild"] = [
    (re.compile(r"error CS\d{4}:", re.IGNORECASE), SeverityLevel.ERROR),
    (re.compile(r"warning CS\d{4}:", re.IGNORECASE), SeverityLevel.WARNING),
]

AZURE_DEVOPS_PATTERNS["nuget"] = [
    (re.compile(r"NU\d{4}:", re.IGNORECASE), SeverityLevel.ERROR),
    (re.compile(r"Package .+ is not compatible", re.IGNORECASE), SeverityLevel.ERROR),
]
```

### Custom Annotation Parsing

```python
import re

def parse_azure_devops_annotations(log_content: str) -> List[Dict[str, Any]]:
    """Parse Azure DevOps annotations for structured information."""
    annotations = []
    
    annotation_pattern = re.compile(r"##\[([^\]]+)\](.+)", re.IGNORECASE)
    
    for line_num, line in enumerate(log_content.split('\n'), 1):
        match = annotation_pattern.search(line)
        if match:
            annotation_type, content = match.groups()
            annotations.append({
                'type': annotation_type,
                'content': content.strip(),
                'line': line_num
            })
    
    return annotations

# Parse annotations
annotations = parse_azure_devops_annotations(log_content)
for ann in annotations:
    print(f"Line {ann['line']}: [{ann['type']}] {ann['content']}")
```

## Testing

The Azure DevOps patterns module is thoroughly tested with:

- **Pattern Matching**: Tests for accurate error detection across all supported languages
- **Stage Detection**: Tests for various Azure DevOps pipeline formats
- **Annotation Parsing**: Tests for Azure DevOps-specific annotations
- **Integration**: Tests with real Azure DevOps log data
- **Performance**: Tests for pattern matching efficiency
- **Edge Cases**: Tests for malformed logs and boundary conditions
