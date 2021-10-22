"""
Models
"""
from django.db import models


class CurrencyExchangeRate(models.Model):
    from_currency_code = models.CharField(max_length=50, default="BTC", blank=True)
    from_currency_name = models.CharField(max_length=50, default="Bitcoin", blank=True)
    to_currency_code = models.CharField(max_length=50, default="USD", blank=True)
    to_currency_name = models.CharField(max_length=50, default="United States Dollar", blank=True)
    exchange_rate = models.DecimalField(max_digits=18, decimal_places=8, blank=True)
    last_refreshed = models.DateTimeField(blank=True)
    time_zone = models.CharField(max_length=10, default="UTC", blank=True)
    bid_price = models.DecimalField(max_digits=18, decimal_places=8, blank=True)
    ask_price = models.DecimalField(max_digits=18, decimal_places=8, blank=True)

    class Meta:
        ordering = ['last_refreshed']
