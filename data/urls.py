from django.conf.urls import patterns, url

from data.views import view_index, view_stock, view_historical
from data.views import view_risers, view_fallers


urlpatterns = patterns('',
    url(r'^index/(?P<ticker>[A-Z0-9]+)/$', view_index),
    url(r'^stock/(?P<exchange>[A-Z0-9]+)/(?P<ticker>[A-Z0-9]+)/$', view_stock),

    url(r'^historical/(?P<exchange>[A-Z0-9]+)/(?P<ticker>[A-Z0-9]+)/' +
        r'(?P<start_date>\d{4}-\d{2}-\d{2})/(?P<end_date>\d{4}-\d{2}-\d{2})/$',
        view_historical),

    url(r'^risers/(?P<number>\d+)/$', view_risers),
    url(r'^fallers/(?P<number>\d+)/$', view_fallers)
)
