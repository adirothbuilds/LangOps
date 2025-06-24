import unittest
from agentops.llm.registry import LLMRegistry

class TestLLMRegistry(unittest.TestCase):
    def test_register_and_get_llm(self):
        @LLMRegistry.register("TestLLM")
        class TestLLM:
            pass

        llm_cls = LLMRegistry.get_llm("TestLLM")
        self.assertIsNotNone(llm_cls)
        self.assertEqual(llm_cls.__name__, "TestLLM")

    def test_list_llms(self):
        @LLMRegistry.register("TestLLM1")
        class TestLLM1:
            pass

        @LLMRegistry.register("TestLLM2")
        class TestLLM2:
            pass

        llm_names = LLMRegistry.list_llms()
        self.assertIn("TestLLM1", llm_names)
        self.assertIn("TestLLM2", llm_names)

if __name__ == "__main__":
    unittest.main()
