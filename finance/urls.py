from users.views import login_view, logout_view, logout_confirm
from users.views import register, profile_page
from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

urlpatterns = patterns('',
    
    url(r'^account/login$',  login_view),
    url(r'^account/logout$', logout_confirm),
    url(r'^account/register$', register),
    url(r'^account/is_logged_in$', profile_page),
    #other patterns
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
    	{'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
)