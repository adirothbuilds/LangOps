# ParserRegistry Documentation

## Overview

`ParserRegistry` is a utility class for registering and managing parser classes in the `agentops.parser` module. It enables you to register parser classes using a decorator and retrieve or list them by name, supporting both inner-module and top-level parser implementations.

## Class: ParserRegistry

### Class Methods

- `register(name=None)`
  - Decorator to register a parser class with an optional name.
  - Args:
    - `name` (str, optional): Name to register the parser under. If not provided, the class name is used.
  - Usage:
  
    ```python
    @ParserRegistry.register()
    class MyParser(BaseParser):
        ...
    
    @ParserRegistry.register('custom_name')
    class AnotherParser(BaseParser):
        ...
    ```

- `get_parser(name)`
  - Retrieve a registered parser class by name.
  - Args:
    - `name` (str): Name of the parser class.
  - Returns: The parser class if found, else `None`.

- `list_parsers()`
  - List all registered parser names.
  - Returns: List of registered parser names as strings.

## Example Usage

```python
from agentops.parser import ParserRegistry, BaseParser

@ParserRegistry.register()
class MyParser(BaseParser):
    def parse(self, data):
        return data

parser_cls = ParserRegistry.get_parser('MyParser')
print(parser_cls)  # <class 'MyParser'>

print(ParserRegistry.list_parsers())  # ['MyParser']
```

## Notes

- Use the decorator on any parser class you want to register.
- You can register multiple parsers, including inner-module and top-level classes.
- Registered parsers can be retrieved and instantiated dynamically by name.
