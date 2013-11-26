from data.models import Exchange, Symbol
from data.cache import get_components


lse, created = Exchange.objects.get_or_create(abbreviation='LSE',
    defaults={'name': 'London Stock Exchange',
              'ticker': 'L'})
lse.save()


ftse100, created = Symbol.objects.get_or_create(ticker='FTSE',
    defaults={'name': 'FTSE 100',
              'exchange': lse,
              'type': Symbol.INDEX})
ftse100.save()


components = get_components(ftse100)
