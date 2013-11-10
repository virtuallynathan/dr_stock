from django.db import connection

from stocks.models import Exchange, Symbol
from data.yahoo.index import scrape


cursor = connection.cursor()
try:
    cursor.execute('drop schema public cascade;')
    cursor.execute('create schema public;')
finally:
    cursor.close()


lse, created = Exchange.objects.get_or_create(abbreviation='LSE',
    defaults={'name': 'London Stock Exchange',
              'reuters_code': 'L'})
lse.save()

ftse100, created = Symbol.objects.get_or_create(ticker='FTSE',
    defaults={'name': 'FTSE 100',
              'exchange': lse})
ftse100.save()


stocks = scrape(ftse100)
stocks.save()

