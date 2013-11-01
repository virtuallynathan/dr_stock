import ystockquote
import datetime
import time

from pprint import pprint

# Get the share price info for one day
def daily_historical_prices(symbol, start_date):
	
	#from_date = "Mon Feb 15 2010"
	#conv = time.strptime(from_date, "%a %b %d %Y")
	#pprint(time.strftime("%Y-%m-%d", conv))

	hist_prices = ystockquote.get_historical_prices(symbol, start_date, start_date)
	prices = hist_prices[start_date]
	open_price = prices['Open']
	close_price = prices['Close']
	high_price = prices['High']
	low_price = prices['Low']
	volume_price = prices['Volume']

	print 'Share Price Information'
	print 'Company:', symbol
	print 'Date:', start_date

	print ''

	print u'Opening Price: \xA3', open_price
	print u'Close Price: \xA3', close_price
	print u'High Price: \xA3', high_price
	print u'Low Price: \xA3', low_price
	print u'Volume: \xA3', volume_price

if __name__ == '__main__':
	daily_historical_prices('GOOG', '2013-01-03')