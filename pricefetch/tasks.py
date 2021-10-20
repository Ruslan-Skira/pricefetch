"""celery tasks"""
import requests
from celery import shared_task
from django.conf import settings

from pricefetch.serializers import FetchpriceSerializer
from rest_framework import serializers


class CurrencyExchangeRateSerializer(serializers.Serializer):




    from_currency_code = serializers.CharField(max_length=10, source='1. From_Currency Code')
    from_currency_name = serializers.CharField(max_length=10, source='2. From_Currency Name')
    to_currency_code = serializers.CharField(max_length=10, source='3. To_Currency Code')
    to_currency_name = serializers.CharField(max_length=10, source='4. To_Currency Name')
    exchange_rate = serializers.DecimalField(max_digits=20, decimal_places=10, source='5. Exchange Rate')
    last_refreshed = serializers.DateTimeField(source='6. Last Refreshed')
    time_zone = serializers.CharField(max_length=10, source='7. Time Zone')
    bid_price = serializers.DecimalField(max_digits=20, decimal_places=10, source='8. Bid Price')
    ask_price = serializers.DecimalField(max_digits=20, decimal_places=10, source='9. Ask Price')

    def to_representation(self, instance):...
    def to_internal_value(self, data):...
    def validate(self, attrs):
        from_currency_code = attrs.get('1. From_Currency Code')
        from_currency_name = attrs.get('2. From_Currency Name')
        to_currency_code = attrs.get('3. To_Currency Code')
        to_currency_name = attrs.get('4. To_Currency Name')
        exchange_rate = attrs.get('5. Exchange Rate')
        last_refreshed = attrs.get('6. Last Refreshed')
        time_zone = attrs.get('7. Time Zone')
        bid_price = attrs.get('8. Bid Price')
        ask_price = attrs.get('9. Ask Price')

class ResponseSerializer(serializers.Serializer):
    realtime_currency_exchange_rate = CurrencyExchangeRateSerializer(source="Realtime Currency Exchange Rate")


    def validate(self, attrs):
        realtime_currency_exchange_rate = attrs.get("Realtime Currency Exchange Rate")






def validate_response(url: str = None):
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









def alphavantage_request(from_currency='BTC', to_currency='USD'):
    """
    Function return parsed data from GET response to  Alphavantage API.
    """
    url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_currency}&to_currency={to_currency}&apikey={settings.ALPHA_VANTAGE_API_KEY}"

    r_json = validate_response(url)


    # TODO: use serializer
    if "Realtime Currency Exchange Rate" in r_json:
        return CurrencyExchangeRateSerializer(data=r_json["Realtime Currency Exchange Rate"])
        # return ResponseSerializer(data=r_json)
    # if "Error Message" in r_json:
    #     serializer = ResponseSerializer(**r_json)



    # if "Realtime Currency Exchange Rate" in r_json:
    #     r_data = r_json['Realtime Currency Exchange Rate']
    #     data = {}
    #     try:
    #         data['from_currency_code'] = r_data.get('1. From_Currency Code')
    #         data['from_currency_name'] = r_data.get('2. From_Currency Name')
    #         data['to_currency_code'] = r_data.get('3. To_Currency Code')
    #         data['to_currency_name'] = r_data.get('4. To_Currency Name')
    #         data['exchange_rate'] = r_data.get('5. Exchange Rate')
    #         data['last_refreshed'] = r_data.get('6. Last Refreshed')
    #         data['time_zone'] = r_data.get('7. Time Zone')
    #         data['bid_price'] = r_data.get('8. Bid Price')
    #         data['ask_price'] = r_data.get('9. Ask Price')
    #         return data
    #     except KeyError as e:
    #         raise UserWarning(f'Key Error {e}')
    #
    # elif "Error Message" in r_json:
    #     raise UserWarning(r_json["Error Message"])
    # else:
    #     raise UserWarning('response 200 but structure not right')


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
