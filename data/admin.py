from django.contrib import admin
from data.models import Exchange, Symbol, Quote, Price

admin.site.register(Exchange)
admin.site.register(Symbol)
admin.site.register(Quote)
admin.site.register(Price)
