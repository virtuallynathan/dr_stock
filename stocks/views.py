import datetime
from django.shortcuts import render

from data.yahoo.index import scrape_index
from data.yahoo.price import scrape_price

from stocks.models import get_symbol, get_exchange, get_company, Symbol, Price


def view_index(request, ticker, template_name='view_index.html'):
	try:
		index = Symbol.objects.get(type=Symbol.INDEX, ticker=ticker)
	except Symbol.DoesNotExist:
		result = {'error': 'That index does not exist!'}
	else:
		# Scrape components if more than a day old
		now = datetime.datetime.utcnow()
		if index.updated.date() < now.date():
			index = scrape_index(index)

		try:
			price = index.price
		except Price.DoesNotExist:
			price = scrape_price(index)
			index.price = price
			price.save()
			index.save()
		else:
			if (now - index.price.updated.replace(tzinfo=None)).total_seconds() > 15 * 60:
				price = scrape_price(index)
				price.save()

		result = {'index': index}

	return render(request, template_name, result)
