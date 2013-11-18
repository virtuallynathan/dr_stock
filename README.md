# Software Engineering Practical

## Dependencies

* Django
* psycopg2
* django-widget-tweaks
* ujson
* requests
* lxml
* pytz

## Project layout

* data/
 * **cache.py** --- main functions for getting stock data. Retrieves from the database if it can, scrapes otherwise.
 * **models.py** --- models for exchanges, symbols, quotes.
 * **views.py** --- JSON API for retrieving stock data.
 * **urls.py** --- routing for the JSON API.
* finance/
 * Main site directory, base templates, routing, etc.
* users/
 * **views.py** --- views for registration and profile page.
 * templates/ --- templates for login, registration, etc.
* stocks/
 * Some of the stuff in data/ used to live here until I moved it.

## JSON API

* `/data/stock/<EXCHANGE>/<TICKER>`
 * `EXCHANGE` is an abbreviation for an exchange, e.g. **LSE** or **NASDAQ**.
 * `TICKER` is a stock ticker, e.g. **GSK** or **MSFT**.
* `/data/index/<TICKER>`
 * `TICKER` is an exchange ticker, e.g. **FTSE**.
