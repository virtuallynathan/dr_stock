from datetime import datetime
from pytz import utc

from data.yahoo.components import scrape_components
from data.yahoo.price import scrape_price
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


def get_price(symbol):
    '''
    Retrieves the price for a symbol. If the price in the database is more
    than 15 minutes old, it is scraped.
    '''
    try:
        price = symbol.price
    except Price.DoesNotExist:
        price = scrape_price(symbol)
    else:
        now = datetime.now(utc)
        if total_seconds(now - price.updated) > 15 * 60:
            price = scrape_price(symbol)
        else:
            return price

    price.symbol = symbol
    price.save()
    return price


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
