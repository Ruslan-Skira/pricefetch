"""celery tasks"""
import requests
from celery import shared_task
from django.conf import settings

from pricefetch.serializers import FetchpriceSerializer
from rest_framework import serializers

class ResponseSerializer(serializers.Serializer):
    realtime_currency_exchange_rate = serializers.JSONField()




    def validate(self, attrs):
        """
        Check the structure and the code of the request.
        :param attrs:
        :type attrs:
        :return:
        :rtype:
        """
        if r.status_code != 200:
            raise UserWarning(r.status_code, " alphavantage response code not equal to 200")





def alphavantage_request(from_currency='BTC', to_currency='USD'):
    """
    Function return parsed data from GET response to  Alphavantage API.
    """
    url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_currency}&to_currency={to_currency}&apikey={settings.ALPHA_VANTAGE_API_KEY}"

    r = requests.get(url)
    if r.status_code != 200:
        raise UserWarning(r.status_code, " alphavantage response code not equal to 200")
    try:
        r_json = r.json()
    except Exception as e:
        raise serializers.ValidationError(e, 'response do not have json() method')

    # TODO: use serializer
    if "Realtime Currency Exchange Rate" in r_json:
        r_data = r_json['Realtime Currency Exchange Rate']
        data = {}
        try:
            data['from_currency_code'] = r_data.get('1. From_Currency Code')
            data['from_currency_name'] = r_data.get('2. From_Currency Name')
            data['to_currency_code'] = r_data.get('3. To_Currency Code')
            data['to_currency_name'] = r_data.get('4. To_Currency Name')
            data['exchange_rate'] = r_data.get('5. Exchange Rate')
            data['last_refreshed'] = r_data.get('6. Last Refreshed')
            data['time_zone'] = r_data.get('7. Time Zone')
            data['bid_price'] = r_data.get('8. Bid Price')
            data['ask_price'] = r_data.get('9. Ask Price')
            return data
        except KeyError as e:
            raise UserWarning(f'Key Error {e}')

    elif "Error Message" in r:
        raise UserWarning(r_json["Error Message"])
    else:
        raise UserWarning('response 200 but structure not right')


#
# def fetch_price_alphavantage(request):
#     """
#     Function fetch currency exchange from alphavantage
#     """
#
#     data = request.data
#     data._mutable = True  # another variant https://docs.djangoproject.com/en/3.1/ref/request-response/#django.http.QueryDict.copy
#     data.update(alphavantage_request())
#     data._mutable = False


@shared_task
def fetch_price_alphavantage_hourly():
    """
    Periodic task running every hour to fetch data from alphavantage website
    """

    data = alphavantage_request()
    hourly_price = FetchpriceSerializer(data=data)  # TODO: try-catch (log error on UserWarning) + create entity
    hourly_price.is_valid()
    hourly_price.save()
