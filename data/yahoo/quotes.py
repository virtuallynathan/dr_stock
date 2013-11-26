'''
Quote scraper for Yahoo Finance
'''
import datetime
from requests import get

from data.models import Symbol, Quote


BASE_URL = 'http://ichart.yahoo.com/table.csv'


def _fetch_quotes(symbol, start_date, end_date):
    if symbol.type == Symbol.INDEX:
        ticker = '^' + symbol.ticker
    else:
        ticker = symbol.ticker
        if symbol.exchange.ticker:
            ticker += '.' + symbol.exchange.ticker

    response = get(BASE_URL, params={'s': ticker,
                                     'a': start_date.month - 1,
                                     'b': start_date.day,
                                     'c': start_date.year,
                                     'd': end_date.month - 1,
                                     'e': end_date.day,
                                     'f': end_date.year,
                                     'g': 'd'},
                   stream=True)
    print response.url
    response.raise_for_status()
    return response


def scrape_quotes(symbol, start_date, end_date):
    response = _fetch_quotes(symbol, start_date, end_date)

    lines = response.iter_lines()
    lines.next()  # Skip the first line

    quotes = []
    for quote in (q.split(',') for q in lines):
        date = quote[0]
        open, high, low, close = (float(x) for x in quote[1:5])
        volume = int(quote[5])
        adj = float(quote[6])

        date = datetime.datetime.strptime(date, '%Y-%m-%d')

        quote = Quote(symbol=symbol, date=date, volume=volume,
                      open=open, close=close, high=high, low=low)

        quotes.append(quote)

    return quotes
