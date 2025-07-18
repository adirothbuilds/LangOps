# Stage Cleaner

## Overview

The `stage_cleaner.py` module provides utilities for cleaning and normalizing stage names from different CI/CD platforms. Each platform has its own conventions and artifacts that need to be cleaned for consistent stage identification.

## Functions

### `default_clean_stage_name(stage_name: str) -> Optional[str]`

Cleans the stage name by stripping whitespace and checking its length.

**Parameters:**

- `stage_name` (str): The stage name to clean

**Returns:**

- `Optional[str]`: The cleaned stage name or None if invalid

**Example:**

```python
from langops.parser.utils.stage_cleaner import default_clean_stage_name

# Valid stage name
clean_name = default_clean_stage_name("  Build Process  ")
print(clean_name)  # "Build Process"

# Invalid stage name (too short)
clean_name = default_clean_stage_name("B")
print(clean_name)  # None

# Empty stage name
clean_name = default_clean_stage_name("")
print(clean_name)  # None
```

### `github_clean_stage_name(stage_name: str) -> Optional[str]`

Cleans stage names from GitHub Actions logs by removing GitHub-specific artifacts.

**Parameters:**

- `stage_name` (str): The GitHub Actions stage name

**Returns:**

- `Optional[str]`: Cleaned stage name or None if invalid

**Cleaning Rules:**

- Removes `##[group]` prefixes
- Removes `Run` prefixes
- Strips whitespace and validates length

**Example:**

```python
from langops.parser.utils.stage_cleaner import github_clean_stage_name

# GitHub Actions group
clean_name = github_clean_stage_name("##[group] Build and Test")
print(clean_name)  # "Build and Test"

# GitHub Actions run command
clean_name = github_clean_stage_name("Run npm install")
print(clean_name)  # "npm install"

# Combined artifacts
clean_name = github_clean_stage_name("##[group] Run build script")
print(clean_name)  # "build script"
```

### `gitlab_clean_stage_name(stage_name: str) -> Optional[str]`

Cleans stage names from GitLab CI logs by removing GitLab-specific artifacts.

**Parameters:**

- `stage_name` (str): The GitLab stage name

**Returns:**

- `Optional[str]`: Cleaned stage name or None if invalid

**Cleaning Rules:**

- Removes `------> Running stage:` prefixes
- Removes `section_start:` prefixes with timestamps
- Removes bracketed suffixes like `[stable]`
- Strips whitespace and validates length

**Example:**

```python
from langops.parser.utils.stage_cleaner import gitlab_clean_stage_name

# GitLab stage prefix
clean_name = gitlab_clean_stage_name("------> Running stage: Test")
print(clean_name)  # "Test"

# GitLab section start
clean_name = gitlab_clean_stage_name("section_start:1234567890: Build")
print(clean_name)  # "Build"

# GitLab with brackets
clean_name = gitlab_clean_stage_name("Deploy [stable]")
print(clean_name)  # "Deploy"
```

### `jenkins_clean_stage_name(stage_name: str) -> Optional[str]`

Cleans Jenkins stage names by removing common artifacts and checking for invalid names.

**Parameters:**

- `stage_name` (str): The Jenkins stage name to clean

**Returns:**

- `Optional[str]`: The cleaned stage name or None if invalid

**Cleaning Rules:**

- Filters out invalid names: `"user"`, `"admin"`, `"system"`, `"sh"`
- Removes numbered prefixes like `"1. "` or `"2) "`
- Removes bracketed suffixes like `"[stable]"`
- Normalizes `"pipeline"` to `"Pipeline"`
- Strips whitespace

**Example:**

```python
from langops.parser.utils.stage_cleaner import jenkins_clean_stage_name

# Jenkins numbered stage
clean_name = jenkins_clean_stage_name("1. Build and Test")
print(clean_name)  # "Build and Test"

# Jenkins with brackets
clean_name = jenkins_clean_stage_name("Deploy [stable]")
print(clean_name)  # "Deploy"

# Invalid Jenkins stage name
clean_name = jenkins_clean_stage_name("user")
print(clean_name)  # None

# Pipeline normalization
clean_name = jenkins_clean_stage_name("pipeline")
print(clean_name)  # "Pipeline"
```

## Stage Name Cleaners Registry

### `STAGE_NAME_CLEANERS`

A dictionary mapping platform names to their corresponding cleaning functions.

**Available Cleaners:**

- `"github_actions"`: `github_clean_stage_name`
- `"gitlab_ci"`: `gitlab_clean_stage_name`
- `"jenkins"`: `jenkins_clean_stage_name`
- `"default"`: `default_clean_stage_name`

**Example:**

```python
from langops.parser.utils.stage_cleaner import STAGE_NAME_CLEANERS

# Use platform-specific cleaner
cleaner = STAGE_NAME_CLEANERS["jenkins"]
clean_name = cleaner("1. Build Process [stable]")
print(clean_name)  # "Build Process"

# Use default cleaner
cleaner = STAGE_NAME_CLEANERS["default"]
clean_name = cleaner("  Custom Stage  ")
print(clean_name)  # "Custom Stage"

# Handle unknown platform
platform = "unknown"
cleaner = STAGE_NAME_CLEANERS.get(platform, STAGE_NAME_CLEANERS["default"])
clean_name = cleaner("Some Stage")
print(clean_name)  # "Some Stage"
```

## Usage Patterns

### Platform-Aware Cleaning

```python
from langops.parser.utils.stage_cleaner import STAGE_NAME_CLEANERS

def clean_stage_name(stage_name: str, platform: str = "default") -> Optional[str]:
    """Clean stage name based on platform."""
    cleaner = STAGE_NAME_CLEANERS.get(platform, STAGE_NAME_CLEANERS["default"])
    return cleaner(stage_name)

# Usage
clean_name = clean_stage_name("##[group] Build", "github_actions")
print(clean_name)  # "Build"
```

### Batch Cleaning

```python
from langops.parser.utils.stage_cleaner import STAGE_NAME_CLEANERS

def clean_stage_names(stage_names: List[str], platform: str) -> List[str]:
    """Clean multiple stage names."""
    cleaner = STAGE_NAME_CLEANERS.get(platform, STAGE_NAME_CLEANERS["default"])
    return [clean_name for stage_name in stage_names 
            if (clean_name := cleaner(stage_name)) is not None]

# Usage
stages = ["##[group] Build", "Run test", "Deploy [prod]"]
clean_stages = clean_stage_names(stages, "github_actions")
print(clean_stages)  # ["Build", "test", "Deploy [prod]"]
```

### Custom Cleaner

```python
from langops.parser.utils.stage_cleaner import STAGE_NAME_CLEANERS

def custom_clean_stage_name(stage_name: str) -> Optional[str]:
    """Custom stage name cleaner."""
    stage_name = stage_name.strip()
    
    # Remove custom prefixes
    stage_name = stage_name.replace("CUSTOM:", "").strip()
    
    # Validate
    if not stage_name or len(stage_name) < 3:
        return None
    
    return stage_name

# Register custom cleaner
STAGE_NAME_CLEANERS["custom"] = custom_clean_stage_name

# Use custom cleaner
clean_name = STAGE_NAME_CLEANERS["custom"]("CUSTOM: Build Process")
print(clean_name)  # "Build Process"
```

## Integration with Pipeline Parsers

The stage cleaners are commonly used by pipeline parsers to normalize stage names:

```python
from langops.parser.utils.stage_cleaner import STAGE_NAME_CLEANERS
from langops.parser.types.pipeline_types import PipelineStage

class PipelineParser:
    def __init__(self, source: str):
        self.source = source
        self.stage_cleaner = STAGE_NAME_CLEANERS.get(source, STAGE_NAME_CLEANERS["default"])
    
    def parse_stage(self, raw_stage_name: str) -> Optional[PipelineStage]:
        """Parse and clean stage name."""
        clean_name = self.stage_cleaner(raw_stage_name)
        if clean_name:
            return PipelineStage(name=clean_name, start_time=None, end_time=None)
        return None
```

## Platform-Specific Considerations

### GitHub Actions

- **Group Markers**: Uses `##[group]` for collapsible sections
- **Run Commands**: Prefixes shell commands with `Run`
- **Step Names**: Usually descriptive and don't need much cleaning

### GitLab CI

- **Section Markers**: Uses `section_start:` with timestamps
- **Stage Indicators**: Uses `------> Running stage:` prefix
- **Environment Tags**: Uses brackets like `[stable]` for environment indicators

### Jenkins

- **Numbered Steps**: Often uses numbered prefixes like `1.` or `2)`
- **Invalid Names**: Filters out system-level names like `user`, `admin`, `sh`
- **Bracketed Info**: Uses brackets for additional information like `[stable]`

## Error Handling

### Safe Cleaning

```python
from langops.parser.utils.stage_cleaner import STAGE_NAME_CLEANERS

def safe_clean_stage_name(stage_name: str, platform: str) -> str:
    """Clean stage name with fallback."""
    if not stage_name:
        return "Unknown Stage"
    
    try:
        cleaner = STAGE_NAME_CLEANERS.get(platform, STAGE_NAME_CLEANERS["default"])
        clean_name = cleaner(stage_name)
        return clean_name if clean_name else stage_name.strip()
    except Exception:
        return stage_name.strip()
```

### Validation

```python
from langops.parser.utils.stage_cleaner import STAGE_NAME_CLEANERS

def validate_stage_name(stage_name: str) -> bool:
    """Validate if stage name is cleanable."""
    if not isinstance(stage_name, str):
        return False
    
    # Try default cleaner
    cleaner = STAGE_NAME_CLEANERS["default"]
    return cleaner(stage_name) is not None
```

## Performance Considerations

- **Regex Performance**: All cleaners use compiled regex patterns for optimal performance
- **Memory Usage**: Cleaners are stateless and memory-efficient
- **Caching**: Consider caching cleaned names for frequently processed stages
- **Batch Processing**: Process multiple stages at once for better performance

## Extensibility

### Adding New Platform Cleaners

```python
from langops.parser.utils.stage_cleaner import STAGE_NAME_CLEANERS

def azure_clean_stage_name(stage_name: str) -> Optional[str]:
    """Clean Azure DevOps stage names."""
    stage_name = stage_name.strip()
    
    # Remove Azure-specific prefixes
    stage_name = re.sub(r"^##\[section\]", "", stage_name)
    stage_name = re.sub(r"^Task\s+:", "", stage_name)
    
    if not stage_name or len(stage_name) < 2:
        return None
    
    return stage_name

# Register the new cleaner
STAGE_NAME_CLEANERS["azure_devops"] = azure_clean_stage_name
```

### Custom Cleaning Rules

```python
import re
from langops.parser.utils.stage_cleaner import STAGE_NAME_CLEANERS

def advanced_clean_stage_name(stage_name: str) -> Optional[str]:
    """Advanced stage name cleaning with custom rules."""
    stage_name = stage_name.strip()
    
    # Multiple cleaning rules
    cleaning_rules = [
        (r"^Step\s+\d+:\s*", ""),  # Remove step numbers
        (r"\s*\[.*?\]\s*$", ""),   # Remove bracketed suffixes
        (r"^\w+:\s*", ""),         # Remove type prefixes
    ]
    
    for pattern, replacement in cleaning_rules:
        stage_name = re.sub(pattern, replacement, stage_name)
    
    # Validate final result
    if not stage_name or len(stage_name) < 2:
        return None
    
    return stage_name.title()  # Title case
```

## Testing

The stage cleaner module is thoroughly tested with 100% code coverage:

- **Platform-Specific Tests**: Tests for each platform's cleaning logic
- **Edge Cases**: Tests for empty strings, whitespace, and invalid inputs
- **Registry Tests**: Tests for cleaner registration and lookup
- **Integration Tests**: Tests with real stage names from various platforms
