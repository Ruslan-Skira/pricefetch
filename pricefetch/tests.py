from datetime import datetime
from pricefetch.models import CurrencyExchangeRate

cur_ex_rate1 = CurrencyExchangeRate(from_currency_code='BTC', from_currency_name="Bitcoin", to_currency_code='USD',
                                    to_currency_name='United States Dollar', exchange_rate='54375.75000000',
                                    last_refreshed=datetime.now(), time_zone='UTC', bid_price='54380.93000000',
                                    ask_price='54380.94000000')
