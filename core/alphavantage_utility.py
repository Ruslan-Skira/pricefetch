"""celery tasks"""
import json
import logging
from typing import Optional

import requests
from django.conf import settings
from rest_framework import serializers

from pricefetch.serializers import CurrencyExchangeRateSerializer

logger = logging.getLogger(__name__)


def validate_response(url: Optional[str] = None) -> json:
    """
    Function validates response.
    :param url: url for requesting alphavantage api.
    :type url: str
    :return: Json with data
    :rtype: json object
    """

    try:
        response = requests.get(url)
    except Exception as e:
        raise serializers.ValidationError(f'Error occurs during requests.get(url): {e}')

    if response.status_code != 200:
        raise serializers.ValidationError(f'response status code are not equal 200 it is {response.status_code}')
    try:
        r_json = response.json()
    except Exception as e:
        raise serializers.ValidationError(f'Response do not have json() method: {e}')
    return r_json


def alphavantage_request(from_currency: str = 'BTC', to_currency: str = 'USD') -> CurrencyExchangeRateSerializer:
    """
    Function return parsed data from GET response to  Alphavantage API.
    """
    url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_currency}&to_currency={to_currency}&apikey={settings.ALPHA_VANTAGE_API_KEY}"

    r_json = validate_response(url)

    if "Realtime Currency Exchange Rate" in r_json:
        return CurrencyExchangeRateSerializer(data=r_json["Realtime Currency Exchange Rate"])
    elif "Error Message" in r_json:
        raise UserWarning(f"alphavantage return Error Message: {r_json['Error Message']}")
