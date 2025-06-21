# agentops.parser Documentation

Welcome to the documentation for the `agentops.parser` module. This package provides a flexible and extensible framework for building, registering, and using parsers for various data and log formats.

## Overview

- **Modular Design:** Easily add new parsers for different formats and use cases.
- **Registry System:** Register and retrieve parsers dynamically using decorators.
- **Base Classes:** Abstract base classes and utilities for consistent parser development.
- **Extensible Filtering:** Built-in support for keyword, log level, and regex-based log filtering.

## Getting Started

- All parsers should inherit from `BaseParser` and implement the `parse` method.
- Register your parser with the `ParserRegistry` using the `@ParserRegistry.register()` decorator.
- Use the registry to retrieve and instantiate parsers by name.

## Documentation Index

- [BaseParser](./baseparser.md): Abstract base class and utilities for all parsers.
- [ParserRegistry](./registry.md): Decorator-based registry for managing parser classes.
- [ErrorParser](./error_parser.md): Example parser for extracting error log lines.

## Example Usage

```python
from agentops.parser import ParserRegistry

# Retrieve a registered parser by name
ParserClass = ParserRegistry.get_parser('ErrorParser')
parser = ParserClass()
result = parser.parse(log_content)
print(result)
```

## Contributing

- Add new parser classes in the `agentops/parser/` directory.
- Document each parser in a separate markdown file in this folder.
- Update this index as new parsers and features are added.

## Future Expansion

This module is designed to grow. Planned features include:

- More built-in parsers for common formats
- Advanced log analysis utilities
- Parser configuration and chaining

---

## Tests Reference

Unit tests for all core parser components are located in:
- `tests/agentops/parser/test_baseparser.py`
- `tests/agentops/parser/test_errorparser.py`
- `tests/agentops/parser/test_registry.py`

These tests ensure the reliability and correctness of the parser framework. Please refer to them for usage examples and to guide your own test development.

For details on each component, see the linked documentation pages above.
