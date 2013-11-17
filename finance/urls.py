from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout

from stocks.views import view_index
from users.views import profile, register


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'finance.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/login/$',  login, {'template_name': 'login.html'}),
    url(r'^accounts/logout/$', logout, {'template_name': 'logout.html'}),
    url(r'^accounts/profile/$', profile, {'template_name': 'profile.html'}),
    url(r'^accounts/register/$', register, {'template_name': 'register.html'}),

    url(r'^index/(?P<ticker>\w+)/$', view_index, {'template_name': 'view_index.html'})
)
