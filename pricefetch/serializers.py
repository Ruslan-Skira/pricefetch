from django.contrib.auth.models import User, Group
from rest_framework import serializers
from pricefetch.models import CurrencyExchangeRate


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
