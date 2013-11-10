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
    company = models.ForeignKey(Company, related_name='symbol', null=True)

    COMPANY = 'C'
    INDEX = 'I'
    TYPES = ((COMPANY, 'Company'), (INDEX, 'Index'))
    type = models.CharField(max_length=1, choices=TYPES, default=COMPANY)

    components = models.ManyToManyField('self',
                                        db_table='symbol_components',
                                        symmetrical=False)

    def code(self):
        if self.type == Symbol.INDEX:
            return '.{0}'.format(self.ticker)
        else:
            return '{0}.{1}'.format(self.ticker, self.exchange.ticker)

    def __unicode__(self):
        return '{0}'.format(self.code())


class Quote(models.Model):
    '''
    Represents a stock price (volume, close, etc) on a given trading day.
    '''
    symbol = models.ForeignKey(Symbol, related_name='quotes')

    date = models.DateField()
    volume = models.BigIntegerField()
    open = models.DecimalField(max_digits=20, decimal_places=4)
    close = models.DecimalField(max_digits=20, decimal_places=4)
    high = models.DecimalField(max_digits=20, decimal_places=4)
    low = models.DecimalField(max_digits=20, decimal_places=4)

    def __unicode__(self):
        return '{0} - {1:%Y-%m-%d} {2}'.format(self.symbol.code(),
                                               self.date,
                                               self.close)


def get_company(name):
    return Company.objects.get(name=name)


def get_exchange(abbreviation):
    return Exchange.objects.get(abbreviation=abbreviation)


def get_symbol(exchange, ticker):
    return Symbol.objects.get(exchange=exchange, ticker=ticker)
