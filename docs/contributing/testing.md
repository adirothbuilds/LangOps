# Testing Guide

LangOps maintains **100% test coverage** to ensure reliability and stability. This guide covers testing practices, running tests, and contributing to the test suite.

## Test Coverage Status

Current test coverage: **100%**

- **170+ tests** covering all major modules
- **Unit tests** for individual components
- **Integration tests** for complex workflows
- **Edge case testing** for robust error handling

## Running Tests

### Basic Test Execution

```bash
# Run all tests
poetry run pytest

# Run with verbose output
poetry run pytest -v

# Run specific test file
poetry run pytest tests/test_parser.py

# Run specific test class
poetry run pytest tests/test_parser.py::TestErrorParser

# Run specific test method
poetry run pytest tests/test_parser.py::TestErrorParser::test_parse_basic_error
```

### Coverage Reports

```bash
# Run tests with coverage
poetry run pytest --cov=langops

# Generate HTML coverage report
poetry run pytest --cov=langops --cov-report=html

# Generate XML coverage report
poetry run pytest --cov=langops --cov-report=xml

# View coverage in terminal
poetry run pytest --cov=langops --cov-report=term-missing
```

### Test Output Options

```bash
# Show test output (print statements)
poetry run pytest -s

# Stop on first failure
poetry run pytest -x

# Show local variables on failure
poetry run pytest -l

# Run tests in parallel
poetry run pytest -n auto
```

## Test Structure

### Directory Structure

```text
tests/
├── __init__.py
├── conftest.py              # Pytest configuration
├── test_core.py            # Core module tests
├── test_parser.py          # Parser tests
├── test_llm.py             # LLM tests
├── test_prompt.py          # Prompt tests
├── test_alert.py           # Alert tests
└── langops/
    ├── parser/
    │   ├── test_utils.py   # Parser utilities tests
    │   └── test_patterns.py # Pattern tests
    └── fixtures/           # Test data files
```

### Test Categories

#### 1. Unit Tests

Test individual functions and methods:

```python
def test_error_parser_basic():
    """Test basic error parsing functionality."""
    parser = ErrorParser()
    result = parser.from_string("ERROR: Test message")
    
    assert len(result) == 1
    assert result[0].level == "ERROR"
    assert "Test message" in result[0].message
```

#### 2. Integration Tests

Test component interactions:

```python
def test_pipeline_parser_integration():
    """Test complete pipeline parsing workflow."""
    parser = PipelineParser(source="jenkins")
    result = parser.parse(jenkins_log_content, extract_stages=True)
    
    assert result.pipeline_name is not None
    assert len(result.stages) > 0
    assert len(result.errors) >= 0
```

#### 3. Edge Case Tests

Test boundary conditions:

```python
def test_parser_empty_content():
    """Test parser with empty content."""
    parser = ErrorParser()
    result = parser.from_string("")
    
    assert len(result) == 0

def test_parser_malformed_content():
    """Test parser with malformed content."""
    parser = ErrorParser()
    result = parser.from_string("Not a valid log format")
    
    assert isinstance(result, list)
```

## Test Fixtures

### Creating Test Data

```python
# tests/conftest.py
import pytest

@pytest.fixture
def sample_jenkins_log():
    """Sample Jenkins log content for testing."""
    return """
Started by user admin
Building in workspace /var/jenkins_home/workspace/test-job
[INFO] Starting Maven build
[ERROR] Failed to compile: cannot find symbol
[ERROR] symbol: method nonExistentMethod()
[FATAL] Build failed with exit code 1
"""

@pytest.fixture
def sample_github_log():
    """Sample GitHub Actions log content for testing."""
    return """
2024-01-01T12:00:00.000Z [INFO] Starting workflow
2024-01-01T12:00:01.000Z [ERROR] Action failed with exit code 1
2024-01-01T12:00:02.000Z [FATAL] Workflow terminated
"""
```

### Using Fixtures

```python
def test_jenkins_parser_with_fixture(sample_jenkins_log):
    """Test Jenkins parser with fixture data."""
    parser = JenkinsParser()
    result = parser.parse(sample_jenkins_log)
    
    assert len(result.errors) > 0
    assert result.pipeline_name is not None
```

## Parametrized Tests

Test multiple scenarios efficiently:

```python
@pytest.mark.parametrize("log_level,expected_severity", [
    ("ERROR", "HIGH"),
    ("WARN", "MEDIUM"),
    ("INFO", "LOW"),
    ("FATAL", "CRITICAL"),
])
def test_severity_mapping(log_level, expected_severity):
    """Test severity mapping for different log levels."""
    parser = ErrorParser()
    result = parser.from_string(f"{log_level}: Test message")
    
    assert result[0].severity == expected_severity
```

## Mock Testing

### Mocking External Dependencies

```python
from unittest.mock import Mock, patch
import pytest

@patch('langops.llm.openai_llm.OpenAI')
def test_openai_llm_integration(mock_openai):
    """Test OpenAI LLM integration with mocking."""
    # Setup mock
    mock_client = Mock()
    mock_openai.return_value = mock_client
    mock_client.chat.completions.create.return_value.choices[0].message.content = "Test response"
    
    # Test
    llm = OpenAILLM(model="gpt-4")
    response = llm.generate([{"role": "user", "content": "Test"}])
    
    assert response == "Test response"
    mock_client.chat.completions.create.assert_called_once()
```

## Performance Testing

### Benchmarking

```python
import time
import pytest

def test_parser_performance():
    """Test parser performance with large log files."""
    parser = ErrorParser()
    large_log = "ERROR: Test message\n" * 10000
    
    start_time = time.time()
    result = parser.from_string(large_log)
    end_time = time.time()
    
    # Should process 10k lines in under 1 second
    assert (end_time - start_time) < 1.0
    assert len(result) == 10000
```

## Error Testing

### Exception Handling

```python
def test_parser_invalid_file():
    """Test parser with invalid file path."""
    parser = ErrorParser()
    
    with pytest.raises(FileNotFoundError):
        parser.from_file("/nonexistent/file.log")

def test_llm_invalid_api_key():
    """Test LLM with invalid API key."""
    with pytest.raises(ValueError):
        OpenAILLM(api_key="invalid_key")
```

## Test Best Practices

### 1. Test Naming

Use descriptive test names:

```python
# Good
def test_jenkins_parser_extracts_build_errors():
    pass

# Bad
def test_parser():
    pass
```

### 2. Test Documentation

Document test purpose:

```python
def test_pipeline_parser_with_stages():
    """Test that pipeline parser correctly extracts stage information.
    
    This test verifies that:
    - Stage names are extracted correctly
    - Stage status is determined properly
    - Errors are associated with correct stages
    """
    pass
```

### 3. Arrange, Act, Assert

Structure tests clearly:

```python
def test_error_parser_severity():
    """Test error severity classification."""
    # Arrange
    parser = ErrorParser()
    log_content = "FATAL: Critical system failure"
    
    # Act
    result = parser.from_string(log_content)
    
    # Assert
    assert len(result) == 1
    assert result[0].severity == "CRITICAL"
```

### 4. Test Independence

Ensure tests don't depend on each other:

```python
def test_parser_state_isolation():
    """Test that parser instances are independent."""
    parser1 = ErrorParser()
    parser2 = ErrorParser()
    
    result1 = parser1.from_string("ERROR: Test 1")
    result2 = parser2.from_string("ERROR: Test 2")
    
    assert result1 != result2
```

## Continuous Integration

### GitHub Actions

Tests run automatically on:

- Pull requests
- Push to main branch
- Scheduled runs (daily)

### Coverage Requirements

- **Minimum coverage**: 100%
- **Coverage must not decrease** in PRs
- **All new code must be tested**

## Writing New Tests

### For New Features

1. Write tests before implementation (TDD)
2. Test both success and failure cases
3. Include edge cases
4. Test with different input types
5. Verify error messages

### For Bug Fixes

1. Write a failing test that reproduces the bug
2. Fix the bug
3. Ensure the test passes
4. Add additional tests for related scenarios

### Test Checklist

- [ ] Test covers new functionality
- [ ] Test covers edge cases
- [ ] Test covers error conditions
- [ ] Test is independent
- [ ] Test has clear documentation
- [ ] Test follows naming conventions
- [ ] Test maintains 100% coverage

## Running Tests in Development

### Pre-commit Testing

```bash
# Install pre-commit hooks
poetry run pre-commit install

# Run pre-commit manually
poetry run pre-commit run --all-files
```

### Watch Mode

```bash
# Install pytest-watch
poetry add pytest-watch --group dev

# Run tests in watch mode
poetry run ptw -- --cov=langops
```

## Debugging Tests

### VS Code Integration

Add to `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Pytest",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "args": ["${workspaceFolder}/tests/", "-v"],
            "console": "integratedTerminal",
            "justMyCode": false
        }
    ]
}
```

### Debug Specific Tests

```bash
# Run with debugger
poetry run python -m pdb -m pytest tests/test_parser.py::test_specific_function

# Add breakpoints in code
import pdb; pdb.set_trace()
```

## Contributing to Tests

### Guidelines

1. **Maintain 100% coverage**
2. **Write clear, descriptive tests**
3. **Test edge cases and error conditions**
4. **Use fixtures for common test data**
5. **Follow existing test patterns**
6. **Document complex test scenarios**

### Review Process

1. All tests must pass
2. Coverage must remain at 100%
3. Tests must be reviewed by maintainers
4. New tests should follow established patterns

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest-cov documentation](https://pytest-cov.readthedocs.io/)
- [Python testing best practices](https://docs.python-guide.org/writing/tests/)
- [Test-driven development](https://testdriven.io/)
