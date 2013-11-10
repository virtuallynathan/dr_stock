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


class Symbol(models.Model):
    '''
    Represents a stock on a certain stock exchange.
    '''
    name = models.CharField(max_length=50)
    ticker = models.CharField(max_length=50)
    exchange = models.ForeignKey(Exchange, related_name='symbol')
    company = models.ForeignKey(Company, related_name='symbol')

    COMPANY = 'C'
    INDEX = 'I'
    TYPES = ((COMPANY, 'Company'), (INDEX, 'Index'))
    type = models.CharField(max_length=1, choices=TYPES, default=COMPANY)

    components = models.ManyToManyField('self',
                                        db_table='symbol_components',
                                        symmetrical=False)

    def code(self):
        if self.type == INDEX:
            return '.{}'.format(self.ticker)
        else:
            return '{}.{}'.format(self.ticker, self.exchange.reuters_code)

    def __unicode__(self):
        return '{} - {}'.format(self.code())


class Quote(models.Model):
    '''
    Represents a stock price (volume, close, etc) on a given trading day.
    '''
    symbol = models.ForeignKey(Symbol, related_name='quotes')

    date = models.DateField()
    volume = models.IntegerField()
    open = models.DecimalField(max_digits=20, decimal_places=4)
    close = models.DecimalField(max_digits=20, decimal_places=4)
    high = models.DecimalField(max_digits=20, decimal_places=4)
    low = models.DecimalField(max_digits=20, decimal_places=4)

    def __unicode__(self):
        return '{} - {%Y-%m-%d} {}'.format(self.symbol.code(),
                                           self.date,
                                           self.close)


def get_company(name):
    return Company.objects.get(name=name)


def get_symbol(exchange, ticker):
    return Symbol.objects.get(exchange=exchange, ticker=ticker)
