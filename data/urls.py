from django.conf.urls import patterns, include, url

from data.views import view_index, view_stock, view_historical


urlpatterns = patterns('',
    url(r'^index/(?P<ticker>[A-Z0-9]+)$', view_index),
    url(r'^stock/(?P<exchange>[A-Z0-9]+)/(?P<ticker>[A-Z0-9]+)$', view_stock),
    url(r'^historical/(?P<exchange>[A-Z0-9]+)/(?P<ticker>[A-Z0-9]+)/' +
    	r'(?P<start_date>\d{4}-\d{2}-\d{2})/(?P<end_date>\d{4}-\d{2}-\d{2})$', view_historical)
)
