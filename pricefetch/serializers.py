"""serializers"""
import logging
from collections import Mapping, OrderedDict
from typing import Dict

from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import get_error_detail, set_value, SkipField
from rest_framework.settings import api_settings

from pricefetch.models import CurrencyExchangeRate

logger = logging.getLogger(__name__)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class FetchpriceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CurrencyExchangeRate
        fields = '__all__'


class CurrencyExchangeRateSerializer(serializers.Serializer):
    """
    Base serializer for Alphavantage api.
    """
    from_currency_code = serializers.CharField(max_length=10, source='1. From_Currency Code')
    from_currency_name = serializers.CharField(max_length=50, source='2. From_Currency Name')
    to_currency_code = serializers.CharField(max_length=10, source='3. To_Currency Code')
    to_currency_name = serializers.CharField(max_length=50, source='4. To_Currency Name')
    exchange_rate = serializers.DecimalField(max_digits=20, decimal_places=10, source='5. Exchange Rate')
    last_refreshed = serializers.DateTimeField(source='6. Last Refreshed')
    time_zone = serializers.CharField(max_length=10, source='7. Time Zone')
    bid_price = serializers.DecimalField(max_digits=20, decimal_places=10, source='8. Bid Price')
    ask_price = serializers.DecimalField(max_digits=20, decimal_places=10, source='9. Ask Price')

    def to_internal_value(self, data: Dict):
        """
        Rewriting base function for mapping alphavantage dict keys and model fields.
        """
        mapping_dict = {
            'from_currency_code': '1. From_Currency Code',
            'from_currency_name': '2. From_Currency Name',
            'to_currency_code': '3. To_Currency Code',
            'to_currency_name': '4. To_Currency Name',
            'exchange_rate': '5. Exchange Rate',
            'last_refreshed': '6. Last Refreshed',
            'time_zone': '7. Time Zone',
            'bid_price': '8. Bid Price',
            'ask_price': '9. Ask Price'
        }
        if not isinstance(data, Mapping):
            message = self.error_messages['invalid'].format(datatype=type(data).__name__)
            raise ValidationError({api_settings.NON_FIELD_ERRORS_KEY: [message]
                                   }, code='invalid')

        ret = OrderedDict()
        errors = OrderedDict()
        fields = self._writable_fields

        for field in fields:
            validate_method = getattr(self, 'validate_' + field.field_name, None)
            primitive_value = data.get(mapping_dict[field.field_name])
            try:
                validated_value = field.run_validation(primitive_value)
                if validate_method is not None:
                    validated_value = validate_method(validated_value)
            except ValidationError as exc:
                errors[field.field_name] = exc.detail
            except DjangoValidationError as exc:
                errors[field.field_name] = get_error_detail(exc)
            except SkipField:
                pass
            else:
                set_value(ret, [field.field_name], validated_value)

        if errors:
            raise ValidationError(errors)

        return ret

    def create(self, validated_data):
        return CurrencyExchangeRate.objects.create(**validated_data)
