# Jenkins Parser JSON Integration for LLM

This document shows how to get JSON output from the Jenkins Parser for LLM analysis.

## Quick Start

```python
from langops.parser.jenkins_parser import JenkinsParser
from langops.core.types import SeverityLevel

# Initialize parser
parser = JenkinsParser()

# Parse logs
result = parser.parse(log_data, min_severity=SeverityLevel.WARNING)

# Get JSON for LLM
json_data = result.model_dump_json(indent=2)
```

## Available Methods

### 1. Basic JSON Output
```python
# Clean JSON using Pydantic serialization
json_output = result.model_dump_json(indent=2)
```

### 2. Custom JSON Structure
```python
# Create custom structure for specific LLM requirements
custom_data = {
    "jenkins_analysis": {
        "total_stages": len(result.stages),
        "stages": [
            {
                "name": stage.name,
                "issues": [
                    {
                        "severity": log.severity.value,
                        "message": log.message,
                        "timestamp": log.timestamp.isoformat() if log.timestamp else None
                    }
                    for log in stage.logs
                ]
            }
            for stage in result.stages
        ]
    }
}
```

### 3. Summary Statistics
```python
# Get summary for large logs
summary = parser.get_stages_summary(result)
# Returns: {"stage_name": {"error": 2, "warning": 1}}
```

## Examples

See:
- `/langops/parser/json_example.py` - Simple usage example
- `/demo/examples/analysis_jenkins_json.py` - Complete demo with LLM integration

## LLM Prompt Template

```python
prompt = f"""Analyze this Jenkins build failure:

```json
{json_data}
```

Please provide:
1. Root cause analysis
2. Fix recommendations
3. Priority order for issues
"""
```

## File Structure

The JSON output follows this structure:

```json
{
  "stages": [
    {
      "name": "Build",
      "logs": [
        {
          "timestamp": "2023-10-01T10:01:00.456000",
          "message": "ERROR Failed to compile",
          "severity": "critical"
        }
      ]
    }
  ]
}
```

## Benefits

- **Structured**: Organized by pipeline stages
- **Typed**: Severity levels and timestamps are properly typed
- **Clean**: Deduplication and filtering applied
- **LLM-Ready**: Perfect format for prompt engineering
- **Extensible**: Easy to add custom fields or transformations
