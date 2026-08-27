from unittest.mock import patch

from django.test import TestCase


class IndexViewTests(TestCase):
    def test_index_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    @patch("charts.views.fetch_prices")
    def test_fetch_renders_chart(self, mock_fetch):
        mock_fetch.return_value = (["bitcoin", "ethereum"], [64073, 1892.33])
        response = self.client.get("/?fetch=1")
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context["chart_image"])