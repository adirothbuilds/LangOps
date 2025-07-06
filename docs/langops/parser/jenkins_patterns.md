# Jenkins Patterns

## Overview

`jenkins_patterns.py` defines regex patterns for detecting Jenkins stages and build steps.

## API Documentation

### Attributes

#### `STAGE_PATTERNS`

**Description**: List of regex patterns for detecting Jenkins stages.

**Type**: `List[Pattern]`

**Examples**:

```python
from langops.parser.jenkins_patterns import STAGE_PATTERNS

log_line = "[Pipeline] stage: 'Build'"
for pattern in STAGE_PATTERNS:
    match = pattern.search(log_line)
    if match:
        print(match.groups())
```

#### `BUILD_STEP_PATTERNS`

**Description**: List of regex patterns for detecting Jenkins build steps.

**Type**: `List[Pattern]`

**Examples**:

```python
from langops.parser.jenkins_patterns import BUILD_STEP_PATTERNS

log_line = "[Pipeline] step: 'Checkout'"
for pattern in BUILD_STEP_PATTERNS:
    match = pattern.search(log_line)
    if match:
        print(match.groups())
```

---

## Usage

Use `STAGE_PATTERNS` and `BUILD_STEP_PATTERNS` to identify Jenkins stages and build steps in log data.

```python
from langops.parser.jenkins_patterns import STAGE_PATTERNS, BUILD_STEP_PATTERNS

log_lines = ["[Pipeline] stage: 'Build'", "[Pipeline] step: 'Checkout'"]
for line in log_lines:
    for pattern in STAGE_PATTERNS + BUILD_STEP_PATTERNS:
        match = pattern.search(line)
        if match:
            print(match.groups())
```

---

## Integration

These patterns are utilized by `JenkinsParser` to extract structured information from Jenkins logs. For example, `JenkinsParser.extract_stage_info` uses `STAGE_PATTERNS` to identify and group stage-related log lines.
