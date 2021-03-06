from django.conf.urls import patterns, include, url
from django.contrib import admin

import data.urls
from users.views import profile, register, login, logout
from finance.views import view_home, view_stock, view_recommendations, view_recommend, view_portfolio

from users.views import favourite_stock, favourite_index, list_favourites
from users.views import unfavourite_stock, unfavourite_index

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^data/', include(data.urls)),

    url(r'^portfolio/$', view_portfolio),
    url(r'^recommend/$', view_recommend),
    url(r'^recommendations/(?P<number>\d+)/$', view_recommendations),
    url(r'^stock/$', view_stock),

    url(r'^accounts/login/$', login, {'template_name': 'login.html'}),
    url(r'^accounts/logout/$', logout, {'template_name': 'logout.html'}),
    url(r'^accounts/profile/$', profile, {'template_name': 'profile.html'}),
    url(r'^accounts/register/$', register, {'template_name': 'register.html'}),
    url(r'^$', view_home),

    # API for favouriting shit
    url(r'^accounts/favourite/(?P<exchange>[A-Z0-9]+)/(?P<ticker>[-A-Z0-9]+)/$', favourite_stock),
    url(r'^accounts/favourite/(?P<ticker>[A-Z0-9]+)/$', favourite_index),
    url(r'^accounts/unfavourite/(?P<exchange>[A-Z0-9]+)/(?P<ticker>[-A-Z0-9]+)/$', unfavourite_stock),
    url(r'^accounts/unfavourite/(?P<ticker>[A-Z0-9]+)/$', unfavourite_index),
    url(r'^accounts/favourites/$', list_favourites),
)
