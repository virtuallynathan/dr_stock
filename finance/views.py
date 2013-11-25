from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from data.models import Quote
from data.views import serialize_symbol, json_response

def view_home(request):
    return render(request, 'home.html')

def view_stock(request):
    return render(request, 'stocks.html')

def view_recommendation(request):

    first_bit_size = 7
    middle_bit_size = 3
    last_bit_size = 1

    return json_response(Quote.objects.all());

def view_portfolio(request):
    return render(request, 'portfolio.html')