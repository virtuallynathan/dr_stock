from django.contrib import admin
from stocks.models import Exchange, Company, Stock, Index

admin.site.register(Exchange)
admin.site.register(Company)
admin.site.register(Stock)
admin.site.register(Index)

