'''
Quote scraper for Yahoo Finance
'''
import datetime
from lxml import etree
from requests import get

from stocks.models import Quote


BASE_URL = 'http://ichart.yahoo.com/table.csv'


def _fetch_quotes(symbol, start_date, end_date):
    return get(BASE_URL, params={'s': symbol,
                                 'a': start_date.month,
                                 'b': start_date.day,
                                 'c': start_date.year,
                                 'd': end_date.month,
                                 'e': end_date.day,
                                 'f': end_date.year,
                                 'g': 'd'},
               stream=True)


def _scrape_quotes(symbol, start_date, end_date):
    response = _fetch_quotes(symbol, start_date, end_date)

    lines = response.iter_lines()
    lines.next()  # Skip the first line

    for quote in (q.split(',') for q in lines):
        print quote
        date, open, high, low, close, volume, adj = quote
        date = datetime.datetime.strptime(date, '%Y-%m-%d')

        yield Quote(date=date, volume=volume, open=open,
                    close=close, high=high, low=low)


def scrape_stock_quotes(stock, start_date, end_date):
    symbol = stock.ticker + stock.exchange.ticker
    return _scrape_quotes(symbol, start_date, end_date)


def scrape_index_quotes(index, start_date, end_date):
    symbol = '^' + index.ticker
    return _scrape_quotes(symbol, start_date, end_date)