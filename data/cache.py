from data.yahoo.quotes import scrape_quotes
from stocks.models import Symbol, Quote


def get_quotes(symbol, start_date, end_date):
	'''
	Retrieves historical quotes for the symbol for the given date range.
	If they're not in the database, it will scrape them.
	'''
	days = (end_date - start_date).days + 1
	expected = days / 7 * 5 + min(days % 7, 5)  # It made sense when I wrote it

	quotes = Quote.objects.filter(symbol=symbol, date__gte=start_date, date__lte=end_date)
	if quotes.count() < expected:
		quotes = scrape_quotes(symbol, start_date, end_date)
		Quote.objects.bulk_create(quotes)

	return quotes
