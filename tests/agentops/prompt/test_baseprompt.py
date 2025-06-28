import unittest
from agentops import BasePrompt
from agentops import PromptRole


class TestBasePrompt(unittest.TestCase):
    def test_add_prompt(self):
        prompt = BasePrompt()
        prompt.add_prompt(
            role=PromptRole.USER, template="Hello, {name}!", variables={"name": "Alice"}
        )
        self.assertEqual(len(prompt.prompts), 1)
        self.assertEqual(prompt.prompts[0]["role"], PromptRole.USER)
        self.assertEqual(prompt.prompts[0]["template"], "Hello, {name}!")
        self.assertEqual(prompt.prompts[0]["variables"], {"name": "Alice"})

    def test_render_prompts(self):
        prompt = BasePrompt()
        prompt.add_prompt(
            role=PromptRole.USER, template="Hello, {name}!", variables={"name": "Alice"}
        )
        rendered = prompt.render_prompts()
        self.assertEqual(len(rendered), 1)
        self.assertEqual(rendered[0]["role"], "user")
        self.assertEqual(rendered[0]["content"], "Hello, Alice!")

    def test_clear_prompts(self):
        prompt = BasePrompt()
        prompt.add_prompt(
            role=PromptRole.USER, template="Hello, {name}!", variables={"name": "Alice"}
        )
        prompt.clear_prompts()
        self.assertEqual(len(prompt.prompts), 0)


if __name__ == "__main__":
    unittest.main()
