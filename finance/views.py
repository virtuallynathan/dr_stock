from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from data.models import Quote

def view_home(request):
    return render(request, 'home.html')

def view_stock(request):
    return render(request, 'stocks.html')

def view_recommendation(request):


    return json_response({'Hello':'World'});

def view_portfolio(request):
    return render(request, 'portfolio.html')