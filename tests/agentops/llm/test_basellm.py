import unittest
from agentops.llm.base import BaseLLM


class TestBaseLLM(unittest.TestCase):
    def test_abstract_methods(self):
        with self.assertRaises(TypeError):
            BaseLLM()

    def test_format_prompt_with_variables(self):
        base_prompt = "Hello, {name}!"
        variables = {"name": "World"}
        formatted_prompt = BaseLLM.format_prompt(base_prompt, variables)
        self.assertEqual(formatted_prompt, "Hello, World!")

    def test_format_prompt_without_variables(self):
        base_prompt = "Hello, World!"
        formatted_prompt = BaseLLM.format_prompt(base_prompt, None)
        self.assertEqual(formatted_prompt, "Hello, World!")


if __name__ == "__main__":
    unittest.main()
