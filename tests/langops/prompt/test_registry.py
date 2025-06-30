import unittest
from langops import PromptRegistry


class TestPromptRegistry(unittest.TestCase):
    def setUp(self):
        PromptRegistry._registry.clear()

    def test_register_and_get_prompt(self):
        class MockPrompt:
            pass

        PromptRegistry.register()(MockPrompt)
        retrieved_prompt = PromptRegistry.get_prompt("MockPrompt")
        self.assertIsNotNone(retrieved_prompt)
        self.assertEqual(retrieved_prompt, MockPrompt)

    def test_register_with_custom_name(self):
        class MockPrompt:
            pass

        PromptRegistry.register("CustomName")(MockPrompt)
        retrieved_prompt = PromptRegistry.get_prompt("CustomName")
        self.assertIsNotNone(retrieved_prompt)
        self.assertEqual(retrieved_prompt, MockPrompt)

    def test_list_prompts(self):
        class MockPrompt1:
            pass

        class MockPrompt2:
            pass

        PromptRegistry.register()(MockPrompt1)
        PromptRegistry.register()(MockPrompt2)
        prompt_list = PromptRegistry.list_prompts()
        self.assertEqual(len(prompt_list), 2)
        self.assertIn("MockPrompt1", prompt_list)
        self.assertIn("MockPrompt2", prompt_list)

    def test_clear_registry(self):
        class MockPrompt:
            pass

        PromptRegistry.register()(MockPrompt)
        self.assertEqual(len(PromptRegistry.list_prompts()), 1)
        PromptRegistry._registry.clear()
        self.assertEqual(len(PromptRegistry.list_prompts()), 0)


if __name__ == "__main__":
    unittest.main()
