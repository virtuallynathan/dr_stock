from stocks.models import Exchange, Index
from data.yahoo.index import scrape

lse = Exchange(name='London Stock Exchange', abbreviation='LSE', reuters_code='L')
lse.save()

ftse100 = Index(name='FTSE 100', exchange=lse, reuters_code='FTSE')
ftse100.save()


stocks = scrape(ftse100)
print stocks

