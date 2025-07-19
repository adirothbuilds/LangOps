# Development Guide

## Setting Up the Development Environment

### Prerequisites

- Python 3.9 or higher
- Poetry (recommended) or pip
- Git

### Clone the Repository

```bash
git clone https://github.com/adirothbuilds/langops.git
cd langops
```

### Install Dependencies

Using Poetry (recommended):

```bash
poetry install
```

Using pip:

```bash
pip install -e ".[dev]"
```

### Development Dependencies

The development environment includes:

- **pytest**: Testing framework
- **coverage**: Code coverage analysis
- **black**: Code formatting
- **flake8**: Linting
- **mypy**: Type checking
- **mkdocs**: Documentation generation
- **pre-commit**: Git hooks

## Project Structure

```text
langops/
├── langops/              # Main package
│   ├── core/            # Core functionality
│   ├── parser/          # Log parsing modules
│   ├── llm/             # LLM integrations
│   ├── prompt/          # Prompt building
│   └── alert/           # Alert systems
├── tests/               # Test suites
├── docs/                # Documentation
├── demo/                # Examples and demos
└── pyproject.toml       # Project configuration
```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

Follow the existing code style and patterns. Key principles:

- **Registry Pattern**: Use registries for extensible components
- **Type Safety**: Use proper type hints
- **Documentation**: Add docstrings and comments
- **Testing**: Write tests for new functionality

### 3. Run Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=langops

# Run specific test file
poetry run pytest tests/test_parser.py
```

### 4. Code Quality

```bash
# Format code
poetry run black langops tests

# Check linting
poetry run flake8 langops tests

# Type checking
poetry run mypy langops
```

### 5. Documentation

Update documentation when adding new features:

```bash
# Build documentation locally
poetry run mkdocs serve

# View at http://localhost:8000
```

## Code Style Guidelines

### Python Style

- Follow PEP 8
- Use type hints
- Maximum line length: 100 characters
- Use descriptive variable names

### Example Code Style

```python
from typing import List, Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class ParseResult:
    """Result of parsing operation.
    
    Attributes:
        errors: List of extracted errors
        warnings: List of warnings
        metadata: Additional parsing metadata
    """
    errors: List[Dict[str, Any]]
    warnings: List[Dict[str, Any]]
    metadata: Optional[Dict[str, Any]] = None
    
    def is_successful(self) -> bool:
        """Check if parsing was successful."""
        return len(self.errors) == 0
```

### Registry Pattern

When adding new parsers or LLMs, use the registry pattern:

```python
from langops.parser.base_parser import BaseParser
from langops.parser.registry import ParserRegistry

class MyCustomParser(BaseParser):
    """Custom parser implementation."""
    
    def parse(self, content: str) -> ParseResult:
        # Implementation here
        pass

# Register the parser
ParserRegistry.register("my_custom", MyCustomParser)
```

## Testing Guidelines

### Test Structure

- Unit tests for individual functions
- Integration tests for complex workflows
- Test files follow pattern: `test_*.py`
- Use descriptive test names

### Writing Tests

```python
import pytest
from langops.parser import ErrorParser

class TestErrorParser:
    """Test suite for ErrorParser."""
    
    def test_parse_basic_error(self):
        """Test parsing a simple error message."""
        parser = ErrorParser()
        result = parser.from_string("ERROR: Something went wrong")
        
        assert len(result) == 1
        assert result[0].level == "ERROR"
        assert "Something went wrong" in result[0].message
    
    def test_parse_empty_content(self):
        """Test parsing empty content."""
        parser = ErrorParser()
        result = parser.from_string("")
        
        assert len(result) == 0
    
    @pytest.mark.parametrize("log_level", ["ERROR", "WARN", "FATAL"])
    def test_parse_different_levels(self, log_level):
        """Test parsing different log levels."""
        parser = ErrorParser()
        result = parser.from_string(f"{log_level}: Test message")
        
        assert len(result) == 1
        assert result[0].level == log_level
```

### Running Tests

```bash
# All tests
poetry run pytest

# Specific test file
poetry run pytest tests/test_parser.py

# Specific test method
poetry run pytest tests/test_parser.py::TestErrorParser::test_parse_basic_error

# With coverage
poetry run pytest --cov=langops --cov-report=html
```

## Adding New Features

### Adding a New Parser

1. Create parser class inheriting from `BaseParser`
2. Implement required methods
3. Add to registry
4. Write tests
5. Update documentation

### Adding a New LLM Integration

1. Create LLM class inheriting from `BaseLLM`
2. Implement required methods
3. Add to registry
4. Write tests
5. Update documentation

### Adding New Patterns

1. Create pattern class inheriting from base pattern
2. Define pattern methods
3. Add to registry
4. Write tests
5. Update documentation

## Documentation

### Updating Documentation

Documentation is built with MkDocs:

```bash
# Install docs dependencies
poetry install

# Serve documentation locally
poetry run mkdocs serve

# Build documentation
poetry run mkdocs build
```

### Documentation Structure

- `docs/`: Main documentation
- `index.md`: Homepage
- `getting-started/`: Installation and quick start
- `docs/langops/`: Module documentation
- `contributing/`: Development guides

## Submitting Changes

### Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests
5. Update documentation
6. Submit pull request

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass
- [ ] Added new tests
- [ ] Coverage maintained

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
```

## Release Process

### Version Bumping

Versions follow semantic versioning (semver):

- **Major**: Breaking changes
- **Minor**: New features
- **Patch**: Bug fixes

### Release Steps

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create release PR
4. Tag release
5. Publish to PyPI

## Getting Help

- Open an issue on GitHub
- Check existing documentation
- Review test examples
- Ask questions in discussions

## Code of Conduct

Please follow the [Code of Conduct](../CODE_OF_CONDUCT.md) when contributing to LangOps.
