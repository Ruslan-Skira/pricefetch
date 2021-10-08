"""celery tasks"""
import requests
from celery import shared_task
from django.conf import settings

from pricefetch.serializers import FetchpriceSerializer


def alphavantage_requesting(from_currency='BTC', to_currency='USD'):
    url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_currency}&to_currency={to_currency}&apikey={settings.ALPHA_VANTAGE_API_KEY}"

    r = requests.get(url)
    if requests.status_codes == '200':
        r_json = r.json()
        if "Realtime Currency Exchange Rate" in r:
            r_data = r_json['Realtime Currency Exchange Rate']
            data = {}
            try:
                data['from_currency_code'] = r_data.get['1. From_Currency Code']
                data['from_currency_name'] = r_data['2. From_Currency Name']
                data['to_currency_code'] = r_data['3. To_Currency Code']
                data['to_currency_name'] = r_data['4. To_Currency Name']
                data['exchange_rate'] = r_data['5. Exchange Rate']
                data['last_refreshed'] = r_data['6. Last Refreshed']
                data['time_zone'] = r_data['7. Time Zone']
                data['bid_price'] = r_data['8. Bid Price']
                data['ask_price'] = r_data['9. Ask Price']
            except KeyError as e:
                raise UserWarning(f'Key Error {e}')

        elif "Error Message" in r:
            raise UserWarning(r_json["Error Message"])


def fetch_price_alphavantage(data=None, from_currency='BTC', to_currency='USD'):
    """function fetch currency exchange from alphavantage"""

    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_currency}&to_currency={to_currency}&apikey={settings.ALPHA_VANTAGE_API_KEY}"
    r = requests.get(url)
    if r.status_code == 200:
        r_data = r.json()['Realtime Currency Exchange Rate']
        data._mutable = True  # another variant https://docs.djangoproject.com/en/3.1/ref/request-response/#django.http.QueryDict.copy
        data['from_currency_code'] = r_data['1. From_Currency Code']
        data['from_currency_name'] = r_data['2. From_Currency Name']
        data['to_currency_code'] = r_data['3. To_Currency Code']
        data['to_currency_name'] = r_data['4. To_Currency Name']
        data['exchange_rate'] = r_data['5. Exchange Rate']
        data['last_refreshed'] = r_data['6. Last Refreshed']
        data['time_zone'] = r_data['7. Time Zone']
        data['bid_price'] = r_data['8. Bid Price']
        data['ask_price'] = r_data['9. Ask Price']
        data._mutable = False

    return data


@shared_task
def fetch_price_alphavantage_hourly(from_currency='BTC', to_currency='USD'):
    """
    Periodic task running every hour to fetch data from alphavantage website
    """
    url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_currency}&to_currency={to_currency}&apikey={settings.ALPHA_VANTAGE_API_KEY}"
    r = requests.get(url)
    r_data = r.json()['Realtime Currency Exchange Rate']
    data = {}
    data['from_currency_code'] = r_data['1. From_Currency Code']
    data['from_currency_name'] = r_data['2. From_Currency Name']
    data['to_currency_code'] = r_data['3. To_Currency Code']
    data['to_currency_name'] = r_data['4. To_Currency Name']
    data['exchange_rate'] = r_data['5. Exchange Rate']
    data['last_refreshed'] = r_data['6. Last Refreshed']
    data['time_zone'] = r_data['7. Time Zone']
    data['bid_price'] = r_data['8. Bid Price']
    data['ask_price'] = r_data['9. Ask Price']
    hourly_price = FetchpriceSerializer(data=data)
    hourly_price.is_valid()
    hourly_price.save()
