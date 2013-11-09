import datetime
from data.yahoo.quotes import scrape_index_quotes
from stocks.models import Index
index = Index(ticker='FTSE')

start_date = datetime.date(year=2012, month=2, day=2)
end_date = datetime.date(year=2012, month=8, day=2)

result = scrape_index_quotes(index, start_date, end_date)

for quote in result:
    print quote

