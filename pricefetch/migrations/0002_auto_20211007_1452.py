# Generated by Django 3.2.8 on 2021-10-07 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pricefetch', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currencyexchangerate',
            name='ask_price',
            field=models.DecimalField(blank=True, decimal_places=8, max_digits=18),
        ),
        migrations.AlterField(
            model_name='currencyexchangerate',
            name='bid_price',
            field=models.DecimalField(blank=True, decimal_places=8, max_digits=18),
        ),
        migrations.AlterField(
            model_name='currencyexchangerate',
            name='exchange_rate',
            field=models.DecimalField(blank=True, decimal_places=8, max_digits=18),
        ),
        migrations.AlterField(
            model_name='currencyexchangerate',
            name='from_currency_code',
            field=models.CharField(blank=True, default='BTC', max_length=50),
        ),
        migrations.AlterField(
            model_name='currencyexchangerate',
            name='from_currency_name',
            field=models.CharField(blank=True, default='Bitcoin', max_length=50),
        ),
        migrations.AlterField(
            model_name='currencyexchangerate',
            name='last_refreshed',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='currencyexchangerate',
            name='time_zone',
            field=models.CharField(blank=True, default='UTC', max_length=10),
        ),
        migrations.AlterField(
            model_name='currencyexchangerate',
            name='to_currency_code',
            field=models.CharField(blank=True, default='USD', max_length=50),
        ),
        migrations.AlterField(
            model_name='currencyexchangerate',
            name='to_currency_name',
            field=models.CharField(blank=True, default='United States Dollar', max_length=50),
        ),
    ]
