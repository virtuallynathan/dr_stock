from django.conf.urls import patterns, include, url

from data.views import view_index, view_stock


urlpatterns = patterns('',
    url(r'^index/(?P<ticker>[A-Z0-9]+)$', view_index),
    url(r'^stock/(?P<exchange>[A-Z0-9]+)/(?P<ticker>[A-Z0-9]+)$', view_stock),
)
