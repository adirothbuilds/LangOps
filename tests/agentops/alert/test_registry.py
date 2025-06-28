import unittest
from agentops import AlertRegistry


class TestAlertRegistry(unittest.TestCase):
    def setUp(self):
        AlertRegistry._registry.clear()

    def test_register_and_get_alert(self):
        class MockAlert:
            pass

        AlertRegistry.register()(MockAlert)
        retrieved_alert = AlertRegistry.get_alert("MockAlert")
        self.assertIsNotNone(retrieved_alert)
        self.assertEqual(retrieved_alert, MockAlert)

    def test_register_with_custom_name(self):
        class MockAlert:
            pass

        AlertRegistry.register("CustomName")(MockAlert)
        retrieved_alert = AlertRegistry.get_alert("CustomName")
        self.assertIsNotNone(retrieved_alert)
        self.assertEqual(retrieved_alert, MockAlert)

    def test_list_alerts(self):
        class MockAlert1:
            pass

        class MockAlert2:
            pass

        AlertRegistry.register()(MockAlert1)
        AlertRegistry.register()(MockAlert2)
        alert_list = AlertRegistry.list_alerts()
        self.assertEqual(len(alert_list), 2)
        self.assertIn("MockAlert1", alert_list)
        self.assertIn("MockAlert2", alert_list)


if __name__ == "__main__":
    unittest.main()
