from django.contrib import auth
from django.template import loader, RequestContext
from django.template import Context
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

def login_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    return render(request, 'login.html')
  

def logout_view(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/account/logged_out")



