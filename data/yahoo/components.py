'''
Component scraper for Yahoo Finance
'''
from lxml import etree
from requests import get

from data.models import Symbol, get_symbol


BASE_URL = 'http://finance.yahoo.com'


def _parse_components(index, html):
    exchange = index.exchange

    for row in html.xpath('//table[@class="yfnc_tableout1"]//tr[./td/@class="yfnc_tabledata1"]'):
        ticker = row[0][0][0].text  # <td><b><a>Symbol</td></b></a>
        dotpos = ticker.rfind('.')
        ticker = ticker[:dotpos] if dotpos > 0 else ticker

        try:
            symbol = get_symbol(exchange, ticker)
        except Symbol.DoesNotExist:
            stock_name = row[1].text
            symbol = Symbol(name=stock_name,
                            ticker=ticker,
                            exchange=exchange,
                            type=Symbol.STOCK)

        yield symbol


def scrape_components(index):
    components = []
    symbol = '^' + index.ticker

    response = get(BASE_URL + '/q/cp', params={'s': symbol})
    response.raise_for_status()

    while True:
        html = etree.HTML(response.text)
        components.extend(_parse_components(index, html))

        next_link = html.xpath('//table[@id="yfncsumtab"]//a[text()="Next"]/@href')
        if len(next_link):
            response = get(BASE_URL + next_link[0])
            response.raise_for_status()
        else:
            break

    return components
