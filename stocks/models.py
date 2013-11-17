import datetime

from django.db import models


class Exchange(models.Model):
    '''
    Represents a stock exchange (e.g. NASDAQ).
    '''
    name = models.CharField(max_length=50)
    abbreviation = models.CharField(max_length=50)
    ticker = models.CharField(max_length=50)

    def __unicode__(self):
        return '{0} - {1}'.format(self.abbreviation, self.name)


class Symbol(models.Model):
    '''
    Represents a stock on a certain stock exchange.
    '''
    name = models.CharField(max_length=50)
    ticker = models.CharField(max_length=50)
    exchange = models.ForeignKey(Exchange, related_name='symbol')

    STOCK = 'S'
    INDEX = 'I'
    TYPES = [(STOCK, 'Stock'), (INDEX, 'Index')]
    type = models.CharField(max_length=1, choices=TYPES, default=STOCK)

    components = models.ManyToManyField('self',
                                        db_table='symbol_components',
                                        symmetrical=False)
    updated = models.DateTimeField(default=datetime.datetime.utcnow)

    class Meta:
        unique_together = (('ticker', 'exchange'),)
        index_together = (('ticker', 'exchange'),)

    def index_code(self):
        return '.{0} - {1}'.format(self.ticker, self.name)

    def stock_code(self):
        return '{0}.{1}'.format(self.ticker, self.exchange.ticker)

    def code(self):
        return self.index_code() if self.type == Symbol.INDEX else self.stock_code()

    def __unicode__(self):
        return self.code()


class Price(models.Model):
    '''
    Represents a real-time stock price (last close, current price, volume, market cap).
    '''
    symbol = models.OneToOneField(Symbol, primary_key=True)
    updated = models.DateTimeField(default=datetime.datetime.utcnow)
    price = models.FloatField()
    last_close = models.FloatField()
    volume = models.BigIntegerField()
    market_cap = models.FloatField(null=True)

    def __unicode__(self):
        return '{0} - {1:%Y-%m-%d} {2}'.format(self.symbol.code(),
                                               self.updated,
                                               self.price)


class Quote(models.Model):
    '''
    Represents a stock price (volume, close, etc) on a given trading day.
    '''
    symbol = models.ForeignKey(Symbol, related_name='quotes')
    date = models.DateField()
    volume = models.BigIntegerField()
    open = models.FloatField()
    close = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()

    class Meta:
        unique_together = (('symbol', 'date'),)
        index_together = (('symbol', 'date'),)

    def __unicode__(self):
        return '{0} - {1:%Y-%m-%d} {2}'.format(self.symbol.code(),
                                               self.date,
                                               self.close)


def get_exchange(abbreviation):
    return Exchange.objects.get(abbreviation=abbreviation)


def get_symbol(exchange, ticker):
    return Symbol.objects.get(exchange=exchange, ticker=ticker)
