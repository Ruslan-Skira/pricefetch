"""
Tests
"""

from unittest.mock import patch

from rest_framework.test import APITestCase

from pricefetch.tasks import alphavantage_requesting


class AlphavantageTest(APITestCase):
    @patch("pricefetch.tasks.alphavantage_requesting.requests.get")
    def test_alphavantage_requesting(self, requests_get):
        requests_get.status_codes = '200'
        alphavantage_requesting()
