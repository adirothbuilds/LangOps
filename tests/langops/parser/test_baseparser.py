from pathlib import Path
import pytest
from langops import BaseParser
import json
import tempfile
import os


class DummyParser(BaseParser):
    def parse(self, data):
        return data.upper()


def test_baseparser_parse():
    parser = DummyParser()
    assert parser.parse("abc") == "ABC"


def test_baseparser_validate_input():
    parser = DummyParser()
    assert parser.validate_input("data") is True
    with pytest.raises(ValueError):
        parser.validate_input(None)
    with pytest.raises(ValueError):
        parser.validate_input(123)
    with pytest.raises(ValueError):
        parser.validate_input([])


def test_baseparser_to_dict():
    parser = DummyParser()
    result = {"a": 1}
    assert parser.to_dict(result) == {"a": 1}


class Obj:
    def __init__(self):
        self.x = 1


def test_baseparser_to_dict_obj():
    parser = DummyParser()
    obj = Obj()
    assert parser.to_dict(obj) == {"x": 1}


def test_baseparser_to_dict_fail():
    parser = DummyParser()
    with pytest.raises(TypeError):
        parser.to_dict(123)


def test_baseparser_to_json():
    parser = DummyParser()
    result = {"a": 1}
    json_str = parser.to_json(result)
    loaded = json.loads(json_str)
    assert loaded == {"a": 1}


def test_baseparser_to_json_fail():
    parser = DummyParser()
    with pytest.raises(ValueError):
        parser.to_json(123)


def test_baseparser_from_file():
    parser = DummyParser()
    with tempfile.NamedTemporaryFile(delete=False, mode="w", encoding="utf-8") as tmp:
        tmp.write("hello")
        tmp_path = tmp.name
    try:
        result = parser.from_file(tmp_path)
        assert result == "HELLO"
    finally:
        os.remove(tmp_path)


def test_baseparser_from_file_not_implemented():
    with pytest.raises(NotImplementedError):
        BaseParser.from_file("fake.txt")

    with pytest.raises(NotImplementedError):
        BaseParser.from_file("fake.txt")


def test_baseparser_to_json_not_implemented():
    with pytest.raises(NotImplementedError):
        BaseParser.to_json({})


def test_handle_log_file(tmp_path: Path):
    file_path = tmp_path / "log.txt"
    file_path.write_text("log content")
    assert DummyParser.handle_log_file(str(file_path)) == "log content"


def test_filter_log_lines_keyword_level_pattern():
    log = "INFO: all good\nERROR: something failed\nDEBUG: details here"
    # keyword
    assert DummyParser.filter_log_lines(log, keyword="ERROR") == [
        "ERROR: something failed"
    ]
    # level
    assert DummyParser.filter_log_lines(log, level="DEBUG") == ["DEBUG: details here"]
    # pattern
    assert DummyParser.filter_log_lines(log, pattern=r"INFO") == ["INFO: all good"]
    # pattern + keyword
    assert DummyParser.filter_log_lines(log, pattern=r"ERROR", keyword="failed") == [
        "ERROR: something failed"
    ]
    # pattern + level (should match both)
    assert DummyParser.filter_log_lines(log, pattern=r"DEBUG", level="DEBUG") == [
        "DEBUG: details here"
    ]
    # nothing matches
    assert DummyParser.filter_log_lines(log, keyword="notfound") == []


def test_to_dict_with_to_dict_method():
    class HasToDict:
        def to_dict(self):
            return {"foo": "bar"}

    obj = HasToDict()
    assert DummyParser.to_dict(obj) == {"foo": "bar"}
