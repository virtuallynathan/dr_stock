from django.db import models


class Company(models.Model):
    '''
    Represents a company. A company may have multiple stocks in multiple exchanges.
    '''
    name = models.CharField()


class Exchange(models.Model):
    '''
    Represents a stock exchange (e.g. NASDAQ).
    '''
    name = models.CharField()
    abbreviation = models.CharField()
    reuters_code = models.CharField()


class Stock(models.Model):
    '''
    Represents a stock on a certain stock exchange.
    '''
    name = models.CharField()
    ticker = models.CharField()
    company = models.ForeignKey(Company, related_name='stocks')
    exchange = models.ForeignKey(Exchange, related_name='stocks')



class Index(models.Model):
    '''
    Represents an index, a collection of stocks, in an exchange (e.g. FTSE 100).
    '''
    name = models.CharField()
    reuters_code = models.CharField()
    stocks = models.ManyToManyField(Stock)



class StockPrice(models.Model):
    '''
    Represents a stock price (volume, close, etc) on a given trading day.
    '''
    stock = models.ForeignKey(Stock, related_name='stock_prices')

    date = models.DateField()
    volume = models.IntegerField()
    open = models.DecimalField()
    close = models.DecimalField()
    high = models.DecimalField()
    low = models.DecimalField()

