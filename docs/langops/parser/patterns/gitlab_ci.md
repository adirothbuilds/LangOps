# GitLab CI Patterns

## Overview

The `gitlab_ci.py` module provides GitLab CI-specific error patterns and pipeline detection rules for parsing GitLab CI logs. These patterns are optimized for GitLab's CI/CD pipeline output format and runner-based build system.

## Pattern Structure

### `GITLAB_CI_PATTERNS`

A dictionary containing language-specific error patterns for GitLab CI pipelines:

```python
GITLAB_CI_PATTERNS = {
    "python": "common.python",   # Reference to common Python patterns
    "nodejs": "common.nodejs",   # Reference to common Node.js patterns
    "java": "common.java",       # Reference to common Java patterns
    # ... more language references
}
```

### `GITLAB_CI_STAGE_PATTERNS`

A list of compiled regex patterns for detecting GitLab CI pipeline stages and jobs:

```python
GITLAB_CI_STAGE_PATTERNS = [
    re.compile(r"\[INFO\]\s+Stage:\s+(.+)", re.IGNORECASE),
    re.compile(r"Executing \"(.+?)\" stage of the job", re.IGNORECASE),
    # ... more stage patterns
]
```

## Language Support

GitLab CI patterns reference common patterns for standard languages:

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

GitLab CI stage patterns identify different phases of pipeline execution:

### Pattern Types

1. **Timestamped Stage Patterns**: `\[\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[.,]?\d*\]\s+\[INFO\]\s+Stage:\s+(.+)`
   - Matches: `[2024-01-01T12:00:00] [INFO] Stage: build`
   - Captures: `build`

2. **Runner Patterns**: `Running with gitlab-runner`
   - Matches: GitLab runner initialization
   - Indicates job start

3. **Job Execution Patterns**: `Executing \"(.+?)\" stage of the job`
   - Matches: `Executing "build" stage of the job`
   - Captures: `build`

4. **Section Patterns**: `section_(start|end):\d+:[a-zA-Z0-9_-]+`
   - Matches: `section_start:1234567890:build_stage`
   - Captures: Section boundaries

5. **GitLab Job Patterns**: `\[gitlab\]\s+\{\s*\((.+?)\)\}`
   - Matches: `[gitlab] { (build_job) }`
   - Captures: `build_job`

6. **GitLab General Patterns**: `\[gitlab\]\s+(.+)`
   - Matches: `[gitlab] Running job build`
   - Captures: `Running job build`

## Usage Examples

### Basic Pattern Matching

```python
from langops.parser.patterns.gitlab_ci import GITLAB_CI_PATTERNS
from langops.parser.utils.resolver import PatternResolver

# Resolve GitLab CI patterns
resolver = PatternResolver()
patterns = resolver.resolve_patterns(GITLAB_CI_PATTERNS)

# Check for errors in a log line
def check_gitlab_ci_errors(log_line: str) -> List[tuple]:
    """Check for GitLab CI-specific errors."""
    errors = []
    
    for language, language_patterns in patterns.items():
        for pattern, severity in language_patterns:
            if pattern.search(log_line):
                errors.append((language, severity, log_line))
    
    return errors

# Example usage
log_line = "ERROR: Could not find a version that satisfies the requirement"
errors = check_gitlab_ci_errors(log_line)
print(errors)  # [('python', SeverityLevel.ERROR, "ERROR: Could not find...")]
```

### Pipeline Stage Extraction

```python
from langops.parser.patterns.gitlab_ci import GITLAB_CI_STAGE_PATTERNS

def extract_gitlab_ci_stages(log_content: str) -> List[Dict[str, Any]]:
    """Extract pipeline stages from GitLab CI logs."""
    stages = []
    lines = log_content.split('\n')
    
    for line_num, line in enumerate(lines, 1):
        for pattern in GITLAB_CI_STAGE_PATTERNS:
            match = pattern.search(line)
            if match and match.groups():
                stages.append({
                    'name': match.group(1),
                    'line': line_num,
                    'pattern': pattern.pattern
                })
                break
    
    return stages

# Extract stages
log_content = """
[2024-01-01T12:00:00] [INFO] Stage: build
Running with gitlab-runner
Executing "test" stage of the job
section_start:1234567890:deploy_stage
[gitlab] { (deploy_job) }
"""
stages = extract_gitlab_ci_stages(log_content)
print(stages)
# [
#     {'name': 'build', 'line': 1, 'pattern': '...'},
#     {'name': 'test', 'line': 3, 'pattern': '...'},
#     {'name': 'deploy_job', 'line': 5, 'pattern': '...'}
# ]
```

### Integration with Pipeline Parser

```python
from langops.parser.patterns.gitlab_ci import GITLAB_CI_PATTERNS, GITLAB_CI_STAGE_PATTERNS
from langops.parser.utils.resolver import PatternResolver

class GitLabCIParser:
    """GitLab CI-specific pipeline parser."""
    
    def __init__(self):
        self.resolver = PatternResolver()
        self.patterns = self.resolver.resolve_patterns(GITLAB_CI_PATTERNS)
        self.stage_patterns = GITLAB_CI_STAGE_PATTERNS
    
    def parse(self, log_content: str) -> Dict[str, Any]:
        """Parse GitLab CI logs."""
        stages = self._extract_stages(log_content)
        errors = self._extract_errors(log_content)
        
        return {
            'source': 'gitlab_ci',
            'stages': stages,
            'errors': errors,
            'metadata': self._extract_metadata(log_content)
        }
    
    def _extract_stages(self, content: str) -> List[str]:
        """Extract pipeline stage names."""
        stages = []
        for line in content.split('\n'):
            for pattern in self.stage_patterns:
                match = pattern.search(line)
                if match and match.groups():
                    stages.append(match.group(1))
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
        """Extract GitLab CI metadata."""
        metadata = {}
        
        # Extract job information
        job_match = re.search(r"Job succeeded", content)
        if job_match:
            metadata['status'] = 'success'
        
        job_fail_match = re.search(r"Job failed", content)
        if job_fail_match:
            metadata['status'] = 'failed'
        
        # Extract runner information
        runner_match = re.search(r"Running with gitlab-runner (\S+)", content)
        if runner_match:
            metadata['runner_version'] = runner_match.group(1)
        
        # Extract project information
        project_match = re.search(r"Getting source from Git repository", content)
        if project_match:
            metadata['source_type'] = 'git'
        
        return metadata
```

## GitLab CI-Specific Considerations

### Pipeline Structure

GitLab CI pipelines are defined in `.gitlab-ci.yml`:

```yaml
stages:
  - build
  - test
  - deploy

build_job:
  stage: build
  script:
    - make build

test_job:
  stage: test
  script:
    - make test

deploy_job:
  stage: deploy
  script:
    - make deploy
```

### Output Format

GitLab CI outputs logs in a specific format:

```text
Running with gitlab-runner 13.0.0 (c127439c)
  on docker-machine b9f5c6f5
Getting source from Git repository
Fetching changes with git depth set to 50...
Initialized empty Git repository in /builds/project/.git/
Created fresh repository.
section_start:1234567890:build_stage
Executing "build" stage of the job script
section_end:1234567890:build_stage
```

### Section Markers

GitLab CI uses section markers for log organization:

- `section_start:timestamp:section_name` - Start of a section
- `section_end:timestamp:section_name` - End of a section
- Sections can be collapsed in the GitLab UI

### Job Execution

GitLab CI job execution follows a pattern:

1. **Runner Selection**: `Running with gitlab-runner`
2. **Source Retrieval**: `Getting source from Git repository`
3. **Stage Execution**: `Executing "stage_name" stage of the job`
4. **Script Execution**: Actual build commands
5. **Job Completion**: `Job succeeded` or `Job failed`

### Stage Detection

GitLab CI stages can be detected through:

- **Timestamped Logs**: `[2024-01-01T12:00:00] [INFO] Stage: build`
- **Job Execution**: `Executing "build" stage of the job`
- **Section Markers**: `section_start:timestamp:build_stage`
- **GitLab Markers**: `[gitlab] { (job_name) }`

## Performance Considerations

- **Pattern Compilation**: All patterns are pre-compiled for performance
- **Common Patterns**: Leverages shared common patterns for efficiency
- **Memory Usage**: Minimal memory footprint due to pattern references
- **Stage Extraction**: Efficient stage boundary detection using sections

## Best Practices

### Pattern Usage

1. **Section Awareness**: Use GitLab's section markers for accurate stage detection
2. **Runner Context**: Consider runner-specific output variations
3. **Error Context**: Include job and stage context for better error understanding
4. **Performance**: Cache resolved patterns for repeated pipeline runs

### Error Handling

```python
from langops.parser.patterns.gitlab_ci import GITLAB_CI_PATTERNS
from langops.parser.utils.resolver import PatternResolver

def safe_gitlab_ci_parsing(log_content: str) -> Dict[str, Any]:
    """Safely parse GitLab CI logs with error handling."""
    try:
        resolver = PatternResolver()
        patterns = resolver.resolve_patterns(GITLAB_CI_PATTERNS)
        
        # Parse with error handling
        return parse_gitlab_ci_logs(log_content, patterns)
    except Exception as e:
        return {
            'error': str(e),
            'source': 'gitlab_ci',
            'stages': [],
            'errors': []
        }
```

## Extensibility

### Adding Custom Patterns

```python
from langops.parser.patterns.gitlab_ci import GITLAB_CI_PATTERNS, GITLAB_CI_STAGE_PATTERNS
from langops.parser.types.pipeline_types import SeverityLevel
import re

# Add custom GitLab CI patterns
GITLAB_CI_PATTERNS["custom"] = [
    (re.compile(r"CUSTOM_GITLAB_ERROR:", re.IGNORECASE), SeverityLevel.ERROR),
    (re.compile(r"CUSTOM_GITLAB_WARNING:", re.IGNORECASE), SeverityLevel.WARNING),
]

# Add custom stage patterns
GITLAB_CI_STAGE_PATTERNS.extend([
    re.compile(r"CUSTOM_SECTION:\s+(.+)", re.IGNORECASE),
])
```

### Runner-Specific Patterns

```python
# Add patterns for specific GitLab runners
GITLAB_CI_PATTERNS["docker"] = [
    (re.compile(r"docker: Error response from daemon", re.IGNORECASE), SeverityLevel.ERROR),
    (re.compile(r"docker: Cannot connect to the Docker daemon", re.IGNORECASE), SeverityLevel.CRITICAL),
]

GITLAB_CI_PATTERNS["kubernetes"] = [
    (re.compile(r"kubectl: error:", re.IGNORECASE), SeverityLevel.ERROR),
    (re.compile(r"pod failed", re.IGNORECASE), SeverityLevel.CRITICAL),
]
```

### Custom Section Handling

```python
import re

def parse_gitlab_sections(log_content: str) -> List[Dict[str, Any]]:
    """Parse GitLab CI sections for better log organization."""
    sections = []
    current_section = None
    
    for line_num, line in enumerate(log_content.split('\n'), 1):
        # Check for section start
        start_match = re.search(r"section_start:(\d+):([a-zA-Z0-9_-]+)", line)
        if start_match:
            timestamp, section_name = start_match.groups()
            current_section = {
                'name': section_name,
                'start_line': line_num,
                'start_timestamp': int(timestamp),
                'lines': []
            }
            continue
        
        # Check for section end
        end_match = re.search(r"section_end:(\d+):([a-zA-Z0-9_-]+)", line)
        if end_match and current_section:
            timestamp, section_name = end_match.groups()
            if section_name == current_section['name']:
                current_section['end_line'] = line_num
                current_section['end_timestamp'] = int(timestamp)
                current_section['duration'] = int(timestamp) - current_section['start_timestamp']
                sections.append(current_section)
                current_section = None
            continue
        
        # Add lines to current section
        if current_section:
            current_section['lines'].append(line)
    
    return sections
```

## Testing

The GitLab CI patterns module is thoroughly tested with:

- **Pattern Matching**: Tests for accurate error detection across all supported languages
- **Stage Detection**: Tests for various GitLab CI pipeline formats
- **Section Parsing**: Tests for section marker handling
- **Integration**: Tests with real GitLab CI log data
- **Performance**: Tests for pattern matching efficiency
- **Edge Cases**: Tests for malformed logs and boundary conditions
