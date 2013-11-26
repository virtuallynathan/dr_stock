from data.models import Exchange, Symbol
from data.cache import get_components


nasdaq, created = Exchange.objects.get_or_create(abbreviation='NASDAQ',
    defaults={'name': 'NASDAQ Stock Market',
              'ticker': ''})
nasdaq.save()


ndx, created = Symbol.objects.get_or_create(ticker='NDX',
    defaults={'name': 'NASDAQ-100',
              'exchange': nasdaq,
              'type': Symbol.INDEX})
ndx.save()


components = get_components(ndx)
