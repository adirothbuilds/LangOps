from agentops.parser.error_parser import ErrorParser
import pytest
import json

LOG_CONTENT = """
2025-06-21 10:00:00 INFO Starting process
2025-06-21 10:01:00 ERROR Failed to connect
2025-06-21 10:02:00 err Disk full
2025-06-21 10:03:00 WARNING Low memory
"""

EMPTY_LOG = """2025-06-21 10:00:00 INFO All good\n2025-06-21 10:03:00 WARNING Low memory\n"""

MIXED_CASE_LOG = """
2025-06-21 10:01:00 Error Something bad
2025-06-21 10:02:00 ERR Another error
2025-06-21 10:03:00 eRrOr Yet another error
"""


def test_errorparser_parse():
    parser = ErrorParser()
    errors = parser.parse(LOG_CONTENT)
    assert len(errors) == 2
    assert "ERROR Failed to connect" in errors[0]
    assert "err Disk full" in errors[1]


def test_errorparser_parse_empty():
    parser = ErrorParser()
    errors = parser.parse(EMPTY_LOG)
    assert errors == []


def test_errorparser_parse_mixed_case():
    parser = ErrorParser()
    errors = parser.parse(MIXED_CASE_LOG)
    assert len(errors) == 3
    assert any("Error Something bad" in e for e in errors)
    assert any("ERR Another error" in e for e in errors)
    assert any("eRrOr Yet another error" in e for e in errors)


def test_errorparser_to_dict():
    parser = ErrorParser()
    errors = parser.parse(LOG_CONTENT)
    d = parser.to_dict(errors)
    assert "errors" in d
    assert len(d["errors"]) == 2


def test_errorparser_to_json():
    parser = ErrorParser()
    errors = parser.parse(LOG_CONTENT)
    json_str = parser.to_json(errors)
    assert '"errors"' in json_str
    assert "ERROR Failed to connect" in json_str
    # Check valid JSON
    loaded = json.loads(json_str)
    assert isinstance(loaded, dict)
    assert "errors" in loaded
    assert len(loaded["errors"]) == 2


def test_errorparser_to_json_empty():
    parser = ErrorParser()
    errors = parser.parse(EMPTY_LOG)
    json_str = parser.to_json(errors)
    loaded = json.loads(json_str)
    assert "errors" in loaded
    assert loaded["errors"] == []


@pytest.mark.parametrize("bad_input", [None, 123, []])
def test_errorparser_validate_input(bad_input):
    parser = ErrorParser()
    with pytest.raises(ValueError):
        parser.validate_input(bad_input)
