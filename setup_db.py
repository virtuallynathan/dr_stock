from stocks.models import Exchange, Index
from data.yahoo.index import scrape

lse, created = Exchange.objects.get_or_create(abbreviation='LSE',
    defaults={'name': 'London Stock Exchange',
              'reuters_code': 'L'})
lse.save()

ftse100, created = Index.objects.get_or_create(reuters_code='FTSE',
    defaults={'name': 'FTSE 100',
              'exchange': lse})
ftse100.save()


stocks = scrape(ftse100)
stocks.save()

