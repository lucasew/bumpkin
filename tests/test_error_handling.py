import logging
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
from bumpkin.sources import eval_node

class TestErrorHandling(unittest.TestCase):
    def setUp(self):
        # We need to capture logs from bumpkin.error which is where report_error logs to.
        # But report_error uses logger = logging.getLogger("bumpkin.error").
        self.logger = logging.getLogger("bumpkin.error")
        # Ensure we capture logs at ERROR level or INFO level?
        # report_error logs at ERROR level by default.

    def test_eval_node_reports_http_error(self):
        # Mock source to raise HTTPError
        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_urlopen.side_effect = HTTPError("http://example.com", 500, "Internal Server Error", {}, None)

            declaration = {
                "_type": "basichttp",
                "url": "http://example.com"
            }
            previous_data = {"some": "data"}

            # Use assertLogs on the logger used by report_error
            with self.assertLogs("bumpkin.error", level="ERROR") as cm:
                result = eval_node(declaration, previous_data)

            # Assert it returns previous data (still swallows for control flow, but reports)
            self.assertEqual(result, previous_data)

            # Assert it logged correctly
            # cm.output is a list of strings like "ERROR:bumpkin.error:Unexpected error: ..."
            self.assertTrue(any("Unexpected error" in r for r in cm.output))
            self.assertTrue(any("HTTP Error 500: Internal Server Error" in r for r in cm.output))
            self.assertTrue(any("Context: {'declaration':" in r for r in cm.output))

    def test_eval_node_reports_generic_exception(self):
        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_urlopen.side_effect = Exception("Generic failure")

            declaration = {
                "_type": "basichttp",
                "url": "http://example.com"
            }
            previous_data = {"some": "data"}

            with self.assertLogs("bumpkin.error", level="ERROR") as cm:
                result = eval_node(declaration, previous_data)

            self.assertEqual(result, previous_data)
            self.assertTrue(any("Unexpected error" in r for r in cm.output))
            self.assertTrue(any("Generic failure" in r for r in cm.output))
            self.assertTrue(any("Context: {'declaration':" in r for r in cm.output))
