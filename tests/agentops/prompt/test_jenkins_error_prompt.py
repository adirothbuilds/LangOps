import unittest
from agentops.prompt.constants import PromptRole
from agentops.prompt.jenkins_error_prompt import JenkinsErrorPrompt


class TestJenkinsErrorPrompt(unittest.TestCase):
    def test_initialization(self):
        jenkins_prompt = JenkinsErrorPrompt(build_id="1234", timestamp="2025-06-26")
        self.assertEqual(len(jenkins_prompt.prompts), 1)
        self.assertEqual(jenkins_prompt.prompts[0]["role"], PromptRole.SYSTEM)
        self.assertIn(
            "Analyzing Jenkins Build Error Logs", jenkins_prompt.prompts[0]["template"]
        )
        self.assertEqual(
            jenkins_prompt.prompts[0]["variables"],
            {"build_id": "1234", "timestamp": "2025-06-26"},
        )

    def test_add_user_prompt(self):
        jenkins_prompt = JenkinsErrorPrompt(build_id="1234", timestamp="2025-06-26")
        error_logs = ["Error 1", "Error 2"]
        jenkins_prompt.add_user_prompt(error_logs)
        self.assertEqual(len(jenkins_prompt.prompts), 3)
        self.assertEqual(jenkins_prompt.prompts[1]["role"], PromptRole.USER)
        self.assertEqual(jenkins_prompt.prompts[1]["variables"], {"log": "Error 1"})
        self.assertEqual(jenkins_prompt.prompts[2]["role"], PromptRole.USER)
        self.assertEqual(jenkins_prompt.prompts[2]["variables"], {"log": "Error 2"})


if __name__ == "__main__":
    unittest.main()
