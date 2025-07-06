# ParserRegistry

## Overview

`ParserRegistry` allows registration and retrieval of parsers by name. It serves as a central hub for managing parser instances in the LangOps SDK.

## API Documentation

### Methods

#### `register(name=None)`

**Description**: Decorator to register a parser class with an optional name.

**Arguments**:

- `name` (str, optional): Name to register the parser under. If not provided, the class name is used.

**Returns**:

- `Type`: The registered parser class.

**Examples**:

```python
from langops.parser.registry import ParserRegistry

@ParserRegistry.register(name="CustomParser")
class CustomParser:
    pass

# Retrieve the parser
parser_cls = ParserRegistry.get("CustomParser")
parser_instance = parser_cls()
```

#### `get(name)`

**Description**: Retrieve a registered parser class by name.

**Arguments**:

- `name` (str): Name of the registered parser.

**Returns**:

- `Type`: The parser class registered under the given name.

**Examples**:

```python
from langops.parser.registry import ParserRegistry

parser_cls = ParserRegistry.get("CustomParser")
parser_instance = parser_cls()
```

---

## Usage

To register a parser, use the `@ParserRegistry.register` decorator. To retrieve a parser, use the `get` method.

```python
from langops.parser.registry import ParserRegistry

@ParserRegistry.register(name="ErrorParser")
class ErrorParser:
    pass

error_parser_cls = ParserRegistry.get("ErrorParser")
error_parser_instance = error_parser_cls()
```

---

## Integration

`ParserRegistry` integrates seamlessly with other modules like `ErrorParser` and `JenkinsParser`. For example, you can register these parsers and use them in a pipeline for comprehensive log analysis.
