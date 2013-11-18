from datetime import datetime

import ujson

from django.http import HttpResponse
from django.shortcuts import render
from data.cache import get_price, get_components, get_quotes
from data.models import Symbol, Exchange, get_exchange, get_symbol


def json_response(response):
    data = ujson.dumps(response)
    return HttpResponse(data, content_type='application/json')


def serialize_price(price):
    return {'price': price.price,
            'last_close': price.last_close,
            'volume': price.volume,
            'market_cap': price.market_cap}


def serialize_symbol(symbol):
    price = get_price(symbol)

    return {'ticker': symbol.ticker,
            'name': symbol.name,
            'exchange': symbol.exchange.abbreviation,
            'price': serialize_price(price)}


def serialize_quote(quote):
    return {'date': quote.date.strftime('%Y-%m-%d'),
            'volume': quote.volume,
            'open': quote.open,
            'close': quote.close,
            'high': quote.high,
            'low': quote.low}


def serialize_historical(symbol, quotes):
    quote_list = [serialize_quote(q) for q in quotes]

    return {'ticker': symbol.ticker,
            'name': symbol.name,
            'exchange': symbol.exchange.abbreviation,
            'historical': quote_list}


def view_index(request, ticker):
    try:
        index = Symbol.objects.get(ticker=ticker)
    except Symbol.DoesNotExist:
        return json_response({'error': 'Index not found'})

    price = get_price(index)
    components = get_components(index)

    result = serialize_symbol(index)
    result['components'] = []

    for component in components:
        symbol = serialize_symbol(component)
        result['components'].append(symbol)

    return json_response(result)


def view_stock(request, exchange, ticker):
    try:
        symbol = Symbol.objects.get(ticker=ticker,
                                    exchange__abbreviation=exchange)
    except Symbol.DoesNotExist:
        return json_response({'error': 'Symbol not found'})

    result = serialize_symbol(symbol)
    return json_response(result)


def view_historical(request, exchange, ticker, start_date, end_date):
    try:
        symbol = Symbol.objects.get(ticker=ticker,
                                    exchange__abbreviation=exchange)
    except Symbol.DoesNotExist:
        return json_response({'error': 'Symbol not found'})

    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    quotes = get_quotes(symbol, start_date, end_date)

    result = serialize_historical(symbol, quotes)
    return json_response(result)
