from django.db import models


class Company(models.Model):
    '''
    Represents a company. A company may have multiple stocks in multiple exchanges.
    '''
    name = models.CharField(max_length=50)


class Exchange(models.Model):
    '''
    Represents a stock exchange (e.g. NASDAQ).
    '''
    name = models.CharField(max_length=50)
    abbreviation = models.CharField(max_length=50)
    reuters_code = models.CharField(max_length=50)


class Stock(models.Model):
    '''
    Represents a stock on a certain stock exchange.
    '''
    name = models.CharField(max_length=50)
    ticker = models.CharField(max_length=50)
    company = models.ForeignKey(Company, related_name='stocks')
    exchange = models.ForeignKey(Exchange, related_name='stocks')



class Index(models.Model):
    '''
    Represents an index, a collection of stocks, in an exchange (e.g. FTSE 100).
    '''
    name = models.CharField(max_length=50)
    reuters_code = models.CharField(max_length=50)
    stocks = models.ManyToManyField(Stock)



class StockPrice(models.Model):
    '''
    Represents a stock price (volume, close, etc) on a given trading day.
    '''
    stock = models.ForeignKey(Stock, related_name='stock_prices')

    date = models.DateField()
    volume = models.IntegerField()
    open = models.DecimalField(max_digits=20, decimal_places=4)
    close = models.DecimalField(max_digits=20, decimal_places=4)
    high = models.DecimalField(max_digits=20, decimal_places=4)
    low = models.DecimalField(max_digits=20, decimal_places=4)

