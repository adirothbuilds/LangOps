import unittest
from langops import LLMResponse


class TestLLMResponse(unittest.TestCase):
    def test_initialization(self):
        response = LLMResponse(
            text="Hello, World!", raw={"key": "value"}, metadata={"latency": 100}
        )
        self.assertEqual(response.text, "Hello, World!")
        self.assertEqual(response.raw, {"key": "value"})
        self.assertEqual(response.metadata, {"latency": 100})

    def test_default_metadata(self):
        response = LLMResponse(text="Hello, World!")
        self.assertEqual(response.metadata, {})

    def test_type_definitions(self):
        self.assertTrue(hasattr(LLMResponse, "__dict__"))


if __name__ == "__main__":
    unittest.main()
