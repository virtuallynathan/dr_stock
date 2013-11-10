import datetime
import sys

from data.yahoo.quotes import scrape_quotes
from stocks.models import Exchange, Symbol, get_symbol, get_exchange


try:
    lse = get_exchange('LSE')
    ftse = get_symbol(lse, 'FTSE')
except:
    print 'Please run the setup script first!'
    sys.exit(1)

start_date = datetime.date(year=2012, month=2, day=2)
end_date = datetime.date(year=2012, month=8, day=2)

result = scrape_quotes(ftse, start_date, end_date)
quotes = list(result)

for quote in quotes:
    print quote
    quote.save()

