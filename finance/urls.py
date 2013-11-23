from django.conf.urls import patterns, include, url
from django.contrib import admin

import data.urls
from users.views import profile, register, send_email, sent, login, logout
from finance.views import view_index, view_home, view_stock
from finance.views import view_historical_data


admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'finance.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^data/', include(data.urls)),

    url(r'^view_index/$', view_index),
    url(r'^stock/(?P<exchange>[A-Z0-9]+)/(?P<ticker>[A-Z0-9]+)/$', view_stock),
    url(r'^view_historical_data/$', view_historical_data),

    url(r'^accounts/login/$', login, {'template_name': 'login.html'}),
    url(r'^accounts/logout/$', logout, {'template_name': 'logout.html'}),
    url(r'^accounts/profile/$', profile, {'template_name': 'profile.html'}),
    url(r'^accounts/updated_profile/$', profile, {'template_name': 'updatedProfile.html'}),
    url(r'^accounts/register/$', register, {'template_name': 'register.html'}),
    url(r'^$', view_home),

    # Messing around with sending email
    url(r'^accounts/email/$',  send_email),
    url(r'^accounts/sent/$',  sent, {'template_name': 'sent.html'}),
)
