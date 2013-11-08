from users.views import login_view, logout_view
from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    
    url(r'^account/login$',  login_view),
    url(r'^account/logout$', logout_view),
    #url(r'^account/logged_in$', logged_in),
)