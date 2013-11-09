from django.db import models


class Company(models.Model):
    '''
    Represents a company. A company may have multiple stocks in multiple exchanges.
    '''
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Exchange(models.Model):
    '''
    Represents a stock exchange (e.g. NASDAQ).
    '''
    name = models.CharField(max_length=50)
    abbreviation = models.CharField(max_length=50)
    reuters_code = models.CharField(max_length=50)

    def __unicode__(self):
        return '{} - {}'.format(self.abbreviation, self.name)


class Stock(models.Model):
    '''
    Represents a stock on a certain stock exchange.
    '''
    name = models.CharField(max_length=50)
    ticker = models.CharField(max_length=50)
    exchange = models.ForeignKey(Exchange, related_name='stocks')
    company = models.ForeignKey(Company, related_name='stocks')

    def __unicode__(self):
        return '{}.{} - {}'.format(self.ticker,
            self.exchange.reuters_code, self.name)


class Index(models.Model):
    '''
    Represents an index, a collection of stocks, in an exchange (e.g. FTSE 100).
    '''
    name = models.CharField(max_length=50)
    ticker = models.CharField(max_length=50)
    exchange = models.ForeignKey(Exchange, related_name='indexes')

    stocks = models.ManyToManyField(Stock)

    def __unicode__(self):
        return '.{} - {}'.format(self.ticker, self.name)


class Quote(models.Model):
    '''
    Represents a stock price (volume, close, etc) on a given trading day.
    '''
    stock = models.ForeignKey(Stock, related_name='quotes')

    date = models.DateField()
    volume = models.IntegerField()
    open = models.DecimalField(max_digits=20, decimal_places=4)
    close = models.DecimalField(max_digits=20, decimal_places=4)
    high = models.DecimalField(max_digits=20, decimal_places=4)
    low = models.DecimalField(max_digits=20, decimal_places=4)

    def __unicode__(self):
        return '{}.{} - {%Y-%m-%d} {}'.format(self.stock.ticker,
            self.stock.exchange.reuters_code, self.date, self.close)


def get_company(name):
    return Company.objects.get(name=name)


def get_stock(exchange, ticker):
    return Stock.objects.get(exchange=exchange, ticker=ticker)
