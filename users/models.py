from django.db import models
#from stocks import models

class Investor(models.Model):
	'''
	Reperesents an investor.
	'''
	investor_id = models.CharField(max_length=30)
	first_name = models.CharField(max_length=30)
	second_name = models.CharField(max_length=30)
	date_of_birth = models.DateField()
	age = models.IntegerField()
	email = models.EmailField()

class Stock(models.Model):
	'''
	Represents a stock on a certain stock exchange.
	'''
	name = models.CharField(max_length=50)
	company = models.CharField(max_length=50)

class StockPrice(models.Model):
	'''
	Represents a stock price on a given day
	'''
	date = models.DateField()
	volume = models.IntegerField()
	open = models.DecimalField(max_digits=20, decimal_places=4)
	close = models.DecimalField(max_digits=20, decimal_places=4)
	high = models.DecimalField(max_digits=20, decimal_places=4)
	low = models.DecimalField(max_digits=20, decimal_places=4)

class StockInfo(models.Model):
	'''
	Represents the stock information a user is interested in
	'''
	stocks = models.ManyToManyField(Stock)
	stock_price = models.ManyToManyField(StockPrice)

class LoginInfo(models.Model):
	'''
	Store the login information for an investor
	'''
	username = models.CharField(max_length=30)
	password = models.CharField(max_length=30)



