import datetime
import sys

from data.cache import get_price, get_quotes
from data.models import get_symbol, get_exchange


try:
    lse = get_exchange('LSE')
    ftse = get_symbol(lse, 'FTSE')
except:
    print 'Please run the setup script first!'
    sys.exit(1)


start_date = datetime.date(year=2012, month=2, day=2)
end_date = datetime.date(year=2012, month=8, day=2)

quotes = get_quotes(ftse, start_date, end_date)

for quote in quotes:
    print quote


for symbol in ftse.components.all():
    price = get_price(symbol)
    print price
