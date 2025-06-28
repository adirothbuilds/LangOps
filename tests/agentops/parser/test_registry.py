from agentops import ParserRegistry
from agentops.parser import ErrorParser


def test_registry_register_and_get():
    parser_cls = ParserRegistry.get_parser("ErrorParser")
    assert parser_cls is ErrorParser
    parser = parser_cls()
    assert hasattr(parser, "parse")


def test_registry_list_parsers():
    names = ParserRegistry.list_parsers()
    assert "ErrorParser" in names
