from datetime import datetime
from pytz import utc

from data.yahoo.components import scrape_components
from data.yahoo.prices import scrape_prices
from data.yahoo.quotes import scrape_quotes
from data.models import Quote, Price


def get_quotes(symbol, start_date, end_date):
    '''
    Retrieves historical quotes for the symbol for the given date range.
    If they're not in the database, it will scrape them.
    '''
    days = (end_date - start_date).days + 1
    expected = days / 7 * 5 + min(days % 7, 5)  # It made sense when I wrote it

    quotes = Quote.objects.filter(symbol=symbol,
                                  date__gte=start_date,
                                  date__lte=end_date)

    if quotes.count() < expected:
        quotes.delete()
        quotes = scrape_quotes(symbol, start_date, end_date)
        Quote.objects.bulk_create(quotes)

    return quotes


def get_components(index):
    '''
    Retrieves the components of an index. If the components in the database
    are more than a day old, it will scrape them.
    '''
    # Scrape components if more than a day old
    now = datetime.now(utc)
    if index.updated.date() < now.date() or not index.components.count():
        components = scrape_components(index)
        for component in components:
            component.save()

        index.components.add(*components)
        index.updated = now
        index.save()
    else:
        components = index.components.all()

    return components


def total_seconds(delta):
    return delta.seconds + delta.days * 24 * 3600


def get_prices(symbols):
    '''
    Retrieves the price for a list of symbols. If any prices in the database
    are more than 15 minutes old, it is scraped.
    '''
    prices = []
    to_update = []
    for symbol in symbols:
        try:
            price = symbol.price
        except Price.DoesNotExist:
            to_update.append(symbol)
        else:
            now = datetime.now(utc)
            if total_seconds(now - price.updated) > 60 * 15:
                to_update.append(symbol)
            else:
                prices.append(price)

    if to_update:
        updated = scrape_prices(to_update)
        for price in updated:
            price.save()
        prices.extend(updated)

    return prices


def get_price(symbol):
    '''
    Retrieves the price for a symbol. If the price in the database is more
    than 15 minutes old, it is scraped.
    '''
    return get_prices([symbol])[0]


def get_risers(number):
    '''
    Retrieves the top 'numer' risers from the database. Doesn't scrape.
    '''
    prices = Price.objects.extra(select={'rise': 'price / last_close'}).order_by('-rise').all()[:number]
    return prices


def get_fallers(number):
    '''
    Retrieves the top 'number' fallers from the database. Doesn't scrape.
    '''
    prices = Price.objects.extra(select={'rise': 'price / last_close'}).order_by('rise').all()[:number]
    return prices


def get_biggest(number):
    '''
    Retrieves the top 'number' stocks by market capitalization. Doesn't scrape.
    '''
    prices = Price.objects.exclude(market_cap__isnull=True).order_by('-market_cap').all()[:number]
    return prices
