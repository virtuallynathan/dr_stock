'''
Quote scraper for Yahoo Finance
'''
import datetime
from lxml import etree
from requests import get

from stocks.models import Symbol, Quote


BASE_URL = 'http://ichart.yahoo.com/table.csv'


def _fetch_quotes(symbol, start_date, end_date):
    if symbol.type == Symbol.INDEX:
        ticker = '^' + symbol.ticker
    else:
        ticker = symbol.ticker + '.' + symbol.exchange.ticker

    response = get(BASE_URL, params={'s': ticker,
                                     'a': start_date.month,
                                     'b': start_date.day,
                                     'c': start_date.year,
                                     'd': end_date.month,
                                     'e': end_date.day,
                                     'f': end_date.year,
                                     'g': 'd'},
                   stream=True)
    response.raise_for_status()
    return response


def scrape_quotes(symbol, start_date, end_date):
    response = _fetch_quotes(symbol, start_date, end_date)

    lines = response.iter_lines()
    lines.next()  # Skip the first line

    for quote in (q.split(',') for q in lines):
        date, open, high, low, close, volume, adj = quote
        date = datetime.datetime.strptime(date, '%Y-%m-%d')

        yield Quote(symbol=symbol, date=date, volume=volume,
                    open=open, close=close, high=high, low=low)
