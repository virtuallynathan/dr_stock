class Index(object):
    '''
    An index is a list of companies in a certain a stock exchange.
    For example, the FTSE 100 in the London Stock Exchange.
    '''
    def __init__(self, name, companies=[]):
        self._companies = set()
        self._companies.extend(companies)

    @property
    def companies(self):
        return frozenset(self._companies)

    @companies.setter
    def companies(self, companies):
        self._companies = frozenset(companies)

    def add_company(self, company):
        self._companies.add(company)

    def remove_company(self, company):
        self._companies.remove(company)

    def __iter__(self):
        return self._companies.__iter()__

    def __contains__(self, company):
        return company in _companies


class Company(object):
    '''
    A company represents a unique company within a stock exchange.
    For example, NYSE/MSFT represents Microsoft in the New York Stock Exchange.
    '''
    def __init__(self, exchange, symbol):
        self._exchange = exchange
        self._symbol = symbol

    @property
    def exchange(self):
        return self._exchange

    @property
    def symbol(self):
        return self._symbol

    def __hash__(self):
        return hash(self._exchange + self._symbol)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __ne__(self, other):
        return not (self == other)


class Stock(object):
    '''
    A stock represents a set of information about a company's share prices
    on a given trading day.
    '''

    _valid_attributes = ['high', 'low', 'opening', 'closing']

    def __init__(self, company, date, **kwargs):
        self._company = company
        self._date = date

        for attribute, value in kwargs.iteritems():
            if attribute not in _valid_attributes:
                raise ValueError('{} is not a valid attribute for a stock'.format(attribute))
            self.__dict__[attribute] = value

    @property
    def company(self):
        return self._company

    @property
    def date(self):
        return self._date

