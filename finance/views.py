from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render

def view_home(request):
	return render(request, 'home.html')

def view_index(request):
	return render(request, 'showIndexes.html')

def view_stock(request, exchange, ticker):
	return render(request, 'showStocks.html', {'exchange': exchange, 'ticker': ticker})

def view_recommendation(request):
	return render(request, 'recommendStock.html')