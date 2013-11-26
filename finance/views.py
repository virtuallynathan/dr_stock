from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render

from datetime import datetime, timedelta
from pytz import utc

from data.cache import get_price
from data.models import Quote, Symbol
from data.views import serialize_symbol, json_response


def view_home(request):
    return render(request, 'home.html')


def view_stock(request):
    return render(request, 'stocks.html')


def view_recommendations(request, number):
    number = int(number)

    c_date_size = 12
    b_date_size = 6
    a_date_size = 3

    today = datetime.now(utc)
    b_start = today - timedelta(b_date_size)
    a_start = b_start - timedelta(a_date_size)
    c_start = a_start - timedelta(c_date_size)

    statement = '''
SELECT * FROM (
WITH tc AS (SELECT symbol_id, Avg(close) FROM data_quote WHERE date >= '{0:%Y-%m-%d}' AND date < '{1:%Y-%m-%d}' GROUP BY symbol_id),
     ta AS (SELECT symbol_id, Avg(close) FROM data_quote WHERE date >= '{1:%Y-%m-%d}' AND date < '{2:%Y-%m-%d}' GROUP BY symbol_id),
     tb AS (SELECT symbol_id, Avg(close) FROM data_quote WHERE date >= '{2:%Y-%m-%d}' AND date <= '{3:%Y-%m-%d}' GROUP BY symbol_id)
       SELECT tc.symbol_id as symbol_id, tc.avg as c, tb.avg as b, ta.avg as a FROM tc
         INNER JOIN ta on tc.symbol_id = ta.symbol_id
         INNER JOIN tb on ta.symbol_id = tb.symbol_id
           WHERE tc.avg > tb.avg AND tb.avg > ta.avg
) t INNER JOIN data_symbol ON id = symbol_id
      ORDER BY ((c - a) * (b - a) * (c - b)) DESC LIMIT {4};
'''.format(c_start, a_start, b_start, today, number)

    symbols = Symbol.objects.raw(statement)

    result = []
    for symbol in symbols:
        price = get_price(symbol)
        result.append(serialize_symbol(symbol, price))

    return json_response(result)


def view_portfolio(request):
    return render(request, 'portfolio.html')

def view_recommend(request):
    return render(request, 'recommend.html')
