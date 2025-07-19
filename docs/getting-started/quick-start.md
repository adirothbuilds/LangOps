# Quick Start

This guide will get you up and running with LangOps in minutes.

## Basic Log Parsing

Start by parsing errors from a log file:

```python
from langops.parser import ErrorParser

# Initialize the parser
parser = ErrorParser()

# Parse errors from a file
errors = parser.from_file("path/to/your/logfile.log")

# Or parse from a string
log_content = """
ERROR: Build failed with exit code 1
WARNING: Deprecated dependency detected
FATAL: Unable to connect to database
"""

errors = parser.from_string(log_content)
print(f"Found {len(errors)} errors")
```

## Pipeline-Specific Parsing

For more advanced parsing with stage detection:

```python
from langops.parser import PipelineParser

# Initialize parser for specific CI/CD platform
parser = PipelineParser(source="jenkins")

# Parse with filtering options
result = parser.parse(
    log_content,
    min_severity="WARNING",
    deduplicate=True,
    extract_stages=True
)

print(f"Pipeline: {result.pipeline_name}")
print(f"Stages: {len(result.stages)}")
print(f"Errors: {len(result.errors)}")
```

## AI-Powered Analysis

Generate intelligent insights from your logs:

```python
from langops.prompt import JenkinsErrorPrompt
from langops.llm import OpenAILLM

# Set up your OpenAI API key
import os
os.environ["OPENAI_API_KEY"] = "your-api-key-here"

# Create a prompt for the errors
prompter = JenkinsErrorPrompt(
    build_id="build_123",
    timestamp="2024-01-01T12:00:00Z"
)

# Add the parsed errors to the prompt
prompter.add_user_prompt(errors)
messages = prompter.render_prompts()

# Get AI analysis
llm = OpenAILLM(model="gpt-4")
response = llm.generate(messages)
print(response)
```

## Working with Different CI/CD Platforms

LangOps supports multiple CI/CD platforms:

### Jenkins

```python
from langops.parser import JenkinsParser

parser = JenkinsParser()
result = parser.parse(jenkins_log_content)
```

### GitHub Actions

```python
from langops.parser import PipelineParser

parser = PipelineParser(source="github")
result = parser.parse(github_actions_log)
```

### GitLab CI

```python
from langops.parser import PipelineParser

parser = PipelineParser(source="gitlab")
result = parser.parse(gitlab_ci_log)
```

## Error Extraction Examples

### Basic Error Extraction

```python
from langops.parser import ErrorParser

parser = ErrorParser()
errors = parser.from_string("""
[ERROR] 2024-01-01 12:00:00 - Database connection failed
[WARN] 2024-01-01 12:00:01 - Slow query detected
[FATAL] 2024-01-01 12:00:02 - Out of memory
""")

for error in errors:
    print(f"Level: {error.level}")
    print(f"Message: {error.message}")
    print(f"Timestamp: {error.timestamp}")
    print("---")
```

### Stage-Aware Parsing

```python
from langops.parser import PipelineParser

parser = PipelineParser(source="jenkins")
result = parser.parse(log_content, extract_stages=True)

for stage in result.stages:
    print(f"Stage: {stage.name}")
    print(f"Status: {stage.status}")
    print(f"Errors: {len(stage.errors)}")
    print("---")
```

## Registry System

LangOps uses a registry system for extensibility:

```python
from langops.parser.registry import ParserRegistry
from langops.llm.registry import LLMRegistry

# List available parsers
print("Available parsers:", ParserRegistry.list())

# List available LLMs
print("Available LLMs:", LLMRegistry.list())

# Get a specific parser
parser = ParserRegistry.get("jenkins")
```

## Working with Patterns

Customize pattern matching for your specific needs:

```python
from langops.parser.patterns import JenkinsPatterns

# Get Jenkins-specific patterns
patterns = JenkinsPatterns()
print("Error patterns:", patterns.get_error_patterns())
print("Stage patterns:", patterns.get_stage_patterns())
```

## Example: Complete Pipeline

Here's a complete example that demonstrates the full LangOps pipeline:

```python
import os
from langops.parser import PipelineParser
from langops.prompt import JenkinsErrorPrompt
from langops.llm import OpenAILLM

# Set up OpenAI API key
os.environ["OPENAI_API_KEY"] = "your-api-key-here"

# Sample Jenkins log
log_content = """
Started by user admin
Building in workspace /var/jenkins_home/workspace/test-job
[INFO] Starting Maven build
[ERROR] Failed to compile: cannot find symbol
[ERROR] symbol: method nonExistentMethod()
[FATAL] Build failed with exit code 1
"""

# Parse the log
parser = PipelineParser(source="jenkins")
result = parser.parse(log_content, min_severity="ERROR")

print(f"Found {len(result.errors)} errors")

# Generate AI analysis
prompter = JenkinsErrorPrompt(build_id="test-123")
prompter.add_user_prompt(result.errors)
messages = prompter.render_prompts()

# Get LLM insights
llm = OpenAILLM(model="gpt-4")
analysis = llm.generate(messages)

print("AI Analysis:")
print(analysis)
```

## Next Steps

- Explore the [Core Modules](../docs/langops/core/index.md) documentation
- Learn about [Parser Deep Dive](../docs/langops/parser/index.md)
- Check out more [examples](../demo/examples/) in the repository
- Learn about [Contributing](../contributing/development.md) to LangOps
