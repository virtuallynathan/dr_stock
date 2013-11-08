from django.template import loader, RequestContext
from django.template import Context
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django import forms
from django.contrib.auth.forms import UserCreationForm

def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
 #    if user is not None:
 #    	if user.is_active:
 #        	print "You provided a correct username and password!"
 #    	else:
 #       		print "Your account has been disabled!"
	# else:
 #    	print "Your username and password were incorrect."
    return render(request, 'login.html', locals(), context_instance = RequestContext(request))
  

def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/account/logout")


def logout_confirm(request):
	return render(request, 'logout.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/is_logged_in")
    else:
        form = UserCreationForm()
    return render(request, "registration.html", {
    	'form': form,
    })
