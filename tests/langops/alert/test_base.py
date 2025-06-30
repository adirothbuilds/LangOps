import unittest
from langops import BaseAlert


class MockAlert(BaseAlert):
    def format_alert(self, data):
        return f"Formatted: {data}"

    def send_alert(self, formatted_data):
        return f"Sent: {formatted_data}"


class TestBaseAlert(unittest.TestCase):
    def test_format_alert(self):
        alert = MockAlert()
        formatted = alert.format_alert("Test Data")
        self.assertEqual(formatted, "Formatted: Test Data")

    def test_send_alert(self):
        alert = MockAlert()
        result = alert.send_alert("Formatted Data")
        self.assertEqual(result, "Sent: Formatted Data")

    def test_validate_input(self):
        self.assertTrue(MockAlert.validate_input({"key": "value"}))
        with self.assertRaises(ValueError):
            MockAlert.validate_input(None)

    def test_from_data(self):
        alert = MockAlert.from_data({"key": "value"})
        self.assertEqual(alert, "Sent: Formatted: {'key': 'value'}")

        with self.assertRaises(NotImplementedError):
            BaseAlert.from_data({"key": "value"})


if __name__ == "__main__":
    unittest.main()
