from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship, backref


Base = declarative_base()


index_stocks = Table('index_stocks',
                     Base.metadata,
                     Column('index_id', Integer, ForeignKey('index.id')),
                     Column('company_id', Integer, ForeignKey('company.id'))


class Mixin(object):
    '''
    Defines common class attributes.
    '''
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


class Exchange(Mixin, Base):
    '''
    Represents a stock exchange (e.g. NASDAQ).
    '''
    name = Column(String)
    abbreviation = Column(String) # TODO - normalise?
    reuters_code = Column(String) # ^

    stocks = relationship('Stock', backref='exchange')
    indexes = relationship('Index', backref='exchange')


class Index(Mixin, Base):
    '''
    Represents an index, a collection of stocks, in an exchange (e.g. FTSE 100).
    '''
    name = Column(String)
    stocks = relationship('Stock', secondary=index_stocks, backref='indexes')

    # TODO - market cap, etc


class Stock(Mixin, Base):
    '''
    Represents a stock on a certain stock exchange.
    '''
    name = Column(String)  # Inherit from company if no special name?
    ticker = Column(String)
    company_id = Column(Integer, ForeignKey('company.id'))
    exchange = Column(Integer, ForeignKey('exchange.id'))

    # Already have a backref to any indexes

    stock_prices = relationship('StockPrice', backref='stock')


class Company(Mixin, Base):
    '''
    Represents a company. A company may have multiple stocks in multiple exchanges.
    '''
    name = Column(String)
    stocks = relationship('Stock', backref='company')


class StockPrice(Mixin, Base):
    '''
    Represents a stock price (volume, close, etc) on a given trading day.
    '''
    stock_id = Column(Integer, ForeignKey('stock.id'))

    date = Column(Date)
    volume = Column(Integer)
    open = Column(Float)
    close = Column(Float)
    high = Column(Float)
    low = Column(Float)

