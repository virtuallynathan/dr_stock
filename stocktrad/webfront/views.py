from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf

# Create your views here.
def login_view (request) :
	c = {}
	c.update(csrf(request))
	return render_to_response('login.html', c)

def auth_view (request) :
	username = request.POST.get('username','')
	password = request.POST.get('password','')
	user = auth.authenticate(username=username, password=password)

	if user is not None:
		auth.login(request, user)
		return HttpResponseRedirect('/dashboard/')
	else:
		return HttpResponseRedirect('/')

def dashboard_view (request) :
	return render_to_response('main.html')