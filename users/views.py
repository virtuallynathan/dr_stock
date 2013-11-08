from django.template import loader, RequestContext
from django.template import Context
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django import forms
from django.contrib.auth.forms import UserCreationForm

# Login in a user and check if they have registered
def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if request.user.is_authenticated():
    	if user.is_active:
    		print "You provided a correct username and password!"
    		return HttpResponseRedirect("account/is_logged_in")
    	else:
    		print "Your account has been disabled"
    else:
    	print "Your username and password were incorrect."
    	return HttpResponseRedirect("account/invalid")
    return render(request, 'login.html', locals(), context_instance = RequestContext(request))
  
# Log a user out
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/account/logout")

# Confirm a user has logged out
def logout_confirm(request):
	return render(request, 'logout.html')

# Allow an investor to register an account
# Does not add to database
def register(request):
    if request.method == 'POST':
        form = UserCreatForm(request.POST)
        if form.is_valid():
            username = form.clean_username()
            password = form.clean_password()
            new_user = form.save()
            user = authenticate(username=username, password =password)
            login(request, user)
            return HttpResponseRedirect("/acount/is_logged_in")
    else:
        form = UserCreationForm()
    return render(request, "registration.html", {
    	'form': form,
    })

# Link to profile page
def profile_page(request):
	return render(Request, "profile.html")