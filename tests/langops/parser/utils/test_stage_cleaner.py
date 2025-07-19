import unittest
from langops.parser.utils.stage_cleaner import (
    default_clean_stage_name,
    github_clean_stage_name,
    gitlab_clean_stage_name,
    jenkins_clean_stage_name,
    STAGE_NAME_CLEANERS,
)


class TestStageCleaner(unittest.TestCase):

    def test_default_clean_stage_name(self):
        """Test default stage name cleaning."""
        # Test valid stage names
        self.assertEqual(default_clean_stage_name("Build"), "Build")
        self.assertEqual(default_clean_stage_name("  Deploy  "), "Deploy")
        self.assertEqual(default_clean_stage_name("Test Stage"), "Test Stage")

        # Test invalid stage names (lines 15-18)
        self.assertIsNone(default_clean_stage_name(""))
        self.assertIsNone(default_clean_stage_name("   "))
        self.assertIsNone(default_clean_stage_name("a"))  # Too short
        self.assertIsNone(default_clean_stage_name("  b  "))  # Too short after strip

        # Test edge cases
        self.assertEqual(default_clean_stage_name("ab"), "ab")  # Minimum valid length
        self.assertEqual(default_clean_stage_name("  ab  "), "ab")

    def test_github_clean_stage_name(self):
        """Test GitHub Actions stage name cleaning."""
        # Test valid stage names
        self.assertEqual(
            github_clean_stage_name("Build Application"), "Build Application"
        )
        self.assertEqual(
            github_clean_stage_name("  Deploy to Production  "), "Deploy to Production"
        )

        # Test GitHub-specific prefixes
        self.assertEqual(
            github_clean_stage_name("##[group] Setup Dependencies"),
            "Setup Dependencies",
        )
        self.assertEqual(
            github_clean_stage_name("##[GROUP] Build Project"), "Build Project"
        )
        self.assertEqual(github_clean_stage_name("Run npm install"), "npm install")
        self.assertEqual(github_clean_stage_name("RUN docker build"), "docker build")

        # Test combined prefixes
        self.assertEqual(github_clean_stage_name("##[group] Run tests"), "tests")

        # Test invalid stage names (lines 31-37)
        self.assertIsNone(github_clean_stage_name(""))
        self.assertIsNone(github_clean_stage_name("   "))
        self.assertIsNone(github_clean_stage_name("##[group]"))  # Empty after cleaning
        self.assertIsNone(github_clean_stage_name("##[group] a"))  # Too short
        self.assertEqual(
            github_clean_stage_name("Run"), "Run"
        )  # "Run" alone is not cleaned
        self.assertEqual(
            github_clean_stage_name("RUN "), "RUN"
        )  # "RUN " also not cleaned (no space requirement met)

        # Test edge cases
        self.assertEqual(
            github_clean_stage_name("##[group] ab"), "ab"
        )  # Minimum valid length
        self.assertEqual(github_clean_stage_name("Run ab"), "ab")

    def test_gitlab_clean_stage_name(self):
        """Test GitLab CI stage name cleaning."""
        # Test valid stage names
        self.assertEqual(gitlab_clean_stage_name("build"), "build")
        self.assertEqual(gitlab_clean_stage_name("  test  "), "test")

        # Test GitLab-specific prefixes and suffixes
        self.assertEqual(
            gitlab_clean_stage_name("-----> Running stage: build"), "build"
        )
        self.assertEqual(gitlab_clean_stage_name("-----> Running stage: test"), "test")
        self.assertEqual(gitlab_clean_stage_name("section_start:123: deploy"), "deploy")
        self.assertEqual(
            gitlab_clean_stage_name("section_start:456789: build_stage"), "build_stage"
        )
        self.assertEqual(gitlab_clean_stage_name("deploy [SUCCESS]"), "deploy ")
        self.assertEqual(gitlab_clean_stage_name("build [FAILED]"), "build ")
        self.assertEqual(gitlab_clean_stage_name("test [WARNING]"), "test ")

        # Test combined cleaning
        self.assertEqual(
            gitlab_clean_stage_name("-----> Running stage: build [SUCCESS]"), "build "
        )
        self.assertEqual(
            gitlab_clean_stage_name("section_start:123: deploy [FAILED]"), "deploy "
        )

        # Test invalid stage names (lines 50-59)
        self.assertIsNone(gitlab_clean_stage_name(""))
        self.assertIsNone(gitlab_clean_stage_name("   "))
        self.assertIsNone(
            gitlab_clean_stage_name("-----> Running stage:")
        )  # Empty after cleaning
        self.assertIsNone(
            gitlab_clean_stage_name("-----> Running stage: a")
        )  # Too short
        self.assertIsNone(
            gitlab_clean_stage_name("section_start:123:")
        )  # Empty after cleaning
        self.assertIsNone(gitlab_clean_stage_name("section_start:123: b"))  # Too short
        self.assertIsNone(gitlab_clean_stage_name("[SUCCESS]"))  # Empty after cleaning

        # Test edge cases
        self.assertEqual(
            gitlab_clean_stage_name("-----> Running stage: ab"), "ab"
        )  # Minimum valid length
        self.assertEqual(gitlab_clean_stage_name("section_start:123: cd"), "cd")

    def test_jenkins_clean_stage_name(self):
        """Test Jenkins stage name cleaning."""
        # Test valid stage names
        self.assertEqual(jenkins_clean_stage_name("Build"), "Build")
        self.assertEqual(jenkins_clean_stage_name("  Deploy  "), "Deploy")
        self.assertEqual(jenkins_clean_stage_name("Test Stage"), "Test Stage")

        # Test Jenkins-specific cleaning
        self.assertEqual(jenkins_clean_stage_name("1. Build"), "Build")
        self.assertEqual(jenkins_clean_stage_name("2) Test"), "Test")
        self.assertEqual(jenkins_clean_stage_name("10. Deploy"), "Deploy")
        self.assertEqual(jenkins_clean_stage_name("Build [SUCCESS]"), "Build")
        self.assertEqual(jenkins_clean_stage_name("Test [FAILED]"), "Test")
        self.assertEqual(jenkins_clean_stage_name("Deploy [UNSTABLE]"), "Deploy")

        # Test combined cleaning
        self.assertEqual(jenkins_clean_stage_name("1. Build [SUCCESS]"), "Build")
        self.assertEqual(jenkins_clean_stage_name("2) Test [FAILED]"), "Test")

        # Test invalid stage names (lines 72-77)
        self.assertIsNone(jenkins_clean_stage_name("user"))
        self.assertIsNone(jenkins_clean_stage_name("USER"))
        self.assertIsNone(jenkins_clean_stage_name("admin"))
        self.assertIsNone(jenkins_clean_stage_name("ADMIN"))
        self.assertIsNone(jenkins_clean_stage_name("system"))
        self.assertIsNone(jenkins_clean_stage_name("SYSTEM"))
        self.assertIsNone(jenkins_clean_stage_name("sh"))
        self.assertIsNone(jenkins_clean_stage_name("SH"))

        # Test special case: "pipeline" becomes "Pipeline"
        self.assertEqual(jenkins_clean_stage_name("pipeline"), "Pipeline")
        self.assertEqual(jenkins_clean_stage_name("PIPELINE"), "Pipeline")
        self.assertEqual(jenkins_clean_stage_name("Pipeline"), "Pipeline")

        # Test edge cases
        self.assertEqual(jenkins_clean_stage_name("ab"), "ab")
        self.assertEqual(jenkins_clean_stage_name("1. ab"), "ab")
        self.assertEqual(
            jenkins_clean_stage_name("Build Pipeline"), "Build Pipeline"
        )  # Contains "pipeline" but not exactly

    def test_stage_name_cleaners_registry(self):
        """Test the STAGE_NAME_CLEANERS registry."""
        # Test all cleaners are registered
        self.assertIn("github_actions", STAGE_NAME_CLEANERS)
        self.assertIn("gitlab_ci", STAGE_NAME_CLEANERS)
        self.assertIn("jenkins", STAGE_NAME_CLEANERS)
        self.assertIn("default", STAGE_NAME_CLEANERS)

        # Test that cleaners are callable
        self.assertTrue(callable(STAGE_NAME_CLEANERS["github_actions"]))
        self.assertTrue(callable(STAGE_NAME_CLEANERS["gitlab_ci"]))
        self.assertTrue(callable(STAGE_NAME_CLEANERS["jenkins"]))
        self.assertTrue(callable(STAGE_NAME_CLEANERS["default"]))

        # Test that cleaners work correctly
        self.assertEqual(
            STAGE_NAME_CLEANERS["github_actions"]("##[group] Build"), "Build"
        )
        self.assertEqual(
            STAGE_NAME_CLEANERS["gitlab_ci"]("-----> Running stage: test"), "test"
        )
        self.assertEqual(STAGE_NAME_CLEANERS["jenkins"]("1. Deploy"), "Deploy")
        self.assertEqual(STAGE_NAME_CLEANERS["default"]("  Clean  "), "Clean")

    def test_edge_cases_all_cleaners(self):
        """Test edge cases for all cleaners."""
        test_cases = [
            ("", None),
            ("   ", None),
            ("a", None),
            ("  b  ", None),
            ("ab", "ab"),
            ("  cd  ", "cd"),
            ("Long Stage Name", "Long Stage Name"),
        ]

        for input_stage, expected in test_cases:
            with self.subTest(input=input_stage):
                self.assertEqual(default_clean_stage_name(input_stage), expected)

                # GitHub cleaner should handle the same basic cases
                if expected is None:
                    self.assertIsNone(github_clean_stage_name(input_stage))
                    self.assertIsNone(gitlab_clean_stage_name(input_stage))
                elif expected not in {"user", "admin", "system", "sh"}:
                    # Jenkins cleaner filters out these specific names
                    result = jenkins_clean_stage_name(input_stage)
                    if input_stage.strip().lower() == "pipeline":
                        self.assertEqual(result, "Pipeline")
                    else:
                        self.assertEqual(result, expected)

    def test_case_insensitive_patterns(self):
        """Test that regex patterns are case insensitive."""
        # GitHub patterns
        self.assertEqual(github_clean_stage_name("##[GROUP] Build"), "Build")
        self.assertEqual(github_clean_stage_name("##[group] Build"), "Build")
        self.assertEqual(github_clean_stage_name("RUN tests"), "tests")
        self.assertEqual(github_clean_stage_name("run tests"), "tests")

        # GitLab patterns
        self.assertEqual(
            gitlab_clean_stage_name("-----> RUNNING STAGE: build"), "build"
        )
        self.assertEqual(
            gitlab_clean_stage_name("-----> running stage: build"), "build"
        )
        self.assertEqual(gitlab_clean_stage_name("SECTION_START:123: deploy"), "deploy")
        self.assertEqual(gitlab_clean_stage_name("section_start:123: deploy"), "deploy")

        # Test bracket removal is case insensitive
        self.assertEqual(gitlab_clean_stage_name("build [success]"), "build ")
        self.assertEqual(gitlab_clean_stage_name("build [SUCCESS]"), "build ")
        self.assertEqual(gitlab_clean_stage_name("build [Failed]"), "build ")

    def test_complex_regex_patterns(self):
        """Test complex regex patterns with various formats."""
        # Test GitLab section_start with different numbers
        self.assertEqual(gitlab_clean_stage_name("section_start:0: init"), "init")
        self.assertEqual(
            gitlab_clean_stage_name("section_start:999999: final"), "final"
        )
        self.assertEqual(
            gitlab_clean_stage_name("section_start:12345: middle"), "middle"
        )

        # Test Jenkins numbered prefixes
        self.assertEqual(jenkins_clean_stage_name("1. Build"), "Build")
        self.assertEqual(jenkins_clean_stage_name("99. Test"), "Test")
        self.assertEqual(jenkins_clean_stage_name("123) Deploy"), "Deploy")

        # Test bracket patterns with various content
        self.assertEqual(jenkins_clean_stage_name("Build [SUCCESS]"), "Build")
        self.assertEqual(jenkins_clean_stage_name("Test [FAILED - 2 failures]"), "Test")
        self.assertEqual(
            jenkins_clean_stage_name("Deploy [UNSTABLE - warnings]"), "Deploy"
        )

        # Test GitLab bracket patterns
        self.assertEqual(gitlab_clean_stage_name("build [status: success]"), "build ")
        self.assertEqual(gitlab_clean_stage_name("test [duration: 5m]"), "test ")

    def test_whitespace_handling(self):
        """Test various whitespace scenarios."""
        # Test leading/trailing whitespace
        self.assertEqual(default_clean_stage_name("   Build   "), "Build")
        self.assertEqual(github_clean_stage_name("   ##[group] Build   "), "Build")
        self.assertEqual(
            gitlab_clean_stage_name("   -----> Running stage: test   "), "test"
        )
        self.assertEqual(jenkins_clean_stage_name("   1. Deploy   "), "Deploy")

        # Test internal whitespace preservation
        self.assertEqual(
            default_clean_stage_name("  Build  Application  "), "Build  Application"
        )
        self.assertEqual(
            github_clean_stage_name("##[group]  Build  App  "), "Build  App"
        )
        self.assertEqual(
            gitlab_clean_stage_name("-----> Running stage:  test  app  "), "test  app"
        )
        self.assertEqual(jenkins_clean_stage_name("1.  Deploy  App  "), "Deploy  App")


if __name__ == "__main__":
    unittest.main()
