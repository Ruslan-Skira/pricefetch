"""
Tests
"""
import unittest
from unittest.mock import patch

from rest_framework.test import APITestCase

from pricefetch.tasks import alphavantage_request


class AlphavantageTest(APITestCase):
    def setUp(self) -> None:
        """
        base data structure
        """
        self.r_data = {
            "Realtime Currency Exchange Rate": {
                "1. From_Currency Code": "BTC",
                "2. From_Currency Name": "Bitcoin",
                "3. To_Currency Code": "USD",
                "4. To_Currency Name": "United States Dollar",
                "5. Exchange Rate": "57462.30000000",
                "6. Last Refreshed": "2021-10-12 09:04:03",
                "7. Time Zone": "UTC",
                "8. Bid Price": "57462.30000000",
                "9. Ask Price": "57462.31000000"
            }
        }

    # @unittest.skip('testing right response')
    @patch("pricefetch.tasks.requests.get")
    def test_alphavantage_return_true(self, requests_get):
        """
        Positive test. Alphavantage response code it 200.
        Checking response data structure.
        :param requests_get:
        :type requests_get:
        :return:
        :rtype:
        """
        # with patch("pricefetch.tasks.requests.get") as
        requests_get.return_value.status_code = 200
        requests_get.return_value = self.r_data
        data = alphavantage_request()
        self.assertContains(data, 'from_currency_code')
