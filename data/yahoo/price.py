'''
Price scraper for Yahoo Finance
'''
from requests import get

from stocks.models import Price, Symbol


BASE_URL = 'http://download.finance.yahoo.com/d/quotes.csv'


def _fetch_price(symbol):
    if symbol.type == Symbol.INDEX:
        ticker = '^' + symbol.ticker
    else:
        ticker = symbol.ticker + '.' + symbol.exchange.ticker

    response = get(BASE_URL, params={'s': ticker, 'f': 'sl1p0v0j1'})  # Or j3 for realtime market cap?
    response.raise_for_status()
    return response


def _parse_market_cap(market_cap):
    if market_cap == 'N/A':
        return None

    mult_dict = {'K': 3, 'M': 6, 'B': 9, 'T': 12}
    mult = mult_dict.get(market_cap[-1], 0)
    return float(market_cap[:-1]) * (10 ** mult)


def scrape_price(symbol):
    print symbol.code()
    response = _fetch_price(symbol)

    line = response.text.strip().split(',')
    assert len(line) == 5

    market_cap = _parse_market_cap(line[4])

    return Price(symbol=symbol, price=line[1], last_close=line[2],
                 volume=line[3], market_cap=market_cap)
