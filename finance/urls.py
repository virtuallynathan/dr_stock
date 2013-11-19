from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout

import data.urls
from users.views import profile, register, send_email, sent
from finance.views import view_index, view_home, view_stock 
from finance.views import view_historical_data


admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'finance.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^data/', include(data.urls)),

    url(r'^home/', view_home),
    url(r'^view_index/', view_index),
    url(r'^view_stock/', view_stock),
    url(r'^view_historical_data/', view_historical_data),

    url(r'^accounts/login/$',  login, {'template_name': 'login.html'}),
    url(r'^accounts/logout/$', logout, {'template_name': 'logout.html'}),
    url(r'^accounts/profile/$', profile, {'template_name': 'profile.html'}),
    url(r'^accounts/register/$', register, {'template_name': 'register.html'}),
    url(r'^$', login, {'template_name': 'login.html'}), 

    # Messing around with sending email
    url(r'^accounts/email/$',  send_email),
    url(r'^accounts/sent/$',  sent, {'template_name': 'sent.html'}),
)
