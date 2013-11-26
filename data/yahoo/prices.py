'''
Price scraper for Yahoo Finance
'''
from itertools import islice
from requests import get

from data.models import Price, Symbol


BASE_URL = 'http://download.finance.yahoo.com/d/quotes.csv'
SYMBOLS_AT_ONCE = 50


def _ticker(symbol):
    if symbol.type == Symbol.INDEX:
        return '^' + symbol.ticker
    else:
        if symbol.exchange.ticker:
            return symbol.ticker + '.' + symbol.exchange.ticker
        else:
            return symbol.ticker


def _fetch_prices(symbols):
    tickers = ','.join(_ticker(s) for s in symbols)
    response = get(BASE_URL, params={'s': tickers, 'f': 'sl1p0v0j1'})
    response.raise_for_status()
    return response


def _parse_market_cap(market_cap):
    if market_cap == 'N/A':
        return None

    mult_dict = {'K': 3, 'M': 6, 'B': 9, 'T': 12}
    mult = mult_dict.get(market_cap[-1], 0)
    return float(market_cap[:-1]) * (10 ** mult)


def split_every(n, iterable):
    '''thanks stackoverflow'''
    i = iter(iterable)
    piece = list(islice(i, n))
    while piece:
        yield piece
        piece = list(islice(i, n))


def scrape_prices(symbols):
    prices = []

    for slice in split_every(SYMBOLS_AT_ONCE, symbols):
        response = _fetch_prices(slice)
        lines = response.iter_lines()
        lines = [l for l in list(lines) if l.strip()]
        assert len(lines) == len(slice)

        for symbol, line in zip(slice, lines):
            line = line.split(',')
            assert len(line) == 5

            market_cap = _parse_market_cap(line[4])

            price = float(line[1])
            last_close = float(line[2])
            volume = float(line[3])

            prices.append(Price(symbol=symbol, price=price, last_close=last_close,
                                volume=volume, market_cap=market_cap))

    return prices
