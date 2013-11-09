from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'stocktrad.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'webfront.views.login_view'),
    url(r'^login/', 'webfront.views.auth_view'),
    url(r'^dashboard/', 'webfront.views.dashboard_view'),
)
