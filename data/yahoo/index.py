'''
Index scraper for Yahoo Finance
'''
from lxml import etree
from requests import get

from stocks.models import Exchange, Stock, Company, get_stock
from data.yahoo.stock import scrape as scrape_stock

BASE_URL = 'http://finance.yahoo.com'

def scrape(index):
    symbol = '.' + index.reuters_code
    response = get(BASE_URL + '/q/cp', params={'s': symbol})
    html = etree.HTML(response.text)

    return fetch_stocks(index, html)


def fetch_stocks(index, html):
    exchange = index.exchange

    for row in html.xpath('//table[@class="yfnc_tableout1"]//tr[td/@class="yfnc_tabledata1"]'):
        stock_symbol = row[0][0][0].text  # <td><b><a>Symbol</td></b></a>
        stock_symbol = stock_symbol[:stock_symbol.lfind('.')]

        try:
            stock = get_stock(exchange, stock_symbol)
        except DoesNotExist:
            stock_name = row[1].text
            company = Company.objects.get_or_create(name=stock_name)
            stock = Stock(name=company_name, ticker=stock_symbol, company=company, exchange=exchange)

        index.stocks.append(stock)

    next_link = html.xpath('//table[@id="yfncsumtab"]//a[text()="Next"]/@href')

    if next_link is not None:
        response = get(BASE_URL + next_link)
        html = etree.HTML(response.text)

        return fetch_stocks(index, html)
    else
        return index
