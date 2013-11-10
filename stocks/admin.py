from django.contrib import admin
from stocks.models import Exchange, Company, Symbol, Quote

admin.site.register(Exchange)
admin.site.register(Company)
admin.site.register(Symbol)
admin.site.register(Quote)

