from django import forms
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, resolve_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.utils.http import is_safe_url

from data.models import Symbol
from data.views import serialize_symbol, json_response


REDIRECT_FIELD_NAME = 'next'
DEFAULT_REDIRECT = '/'


@csrf_protect
@never_cache
def register(request, template_name='register.html'):
    redirect_to = request.POST.get(REDIRECT_FIELD_NAME,
                                   request.GET.get(REDIRECT_FIELD_NAME, ''));

    if not is_safe_url(url=redirect_to, host=request.get_host()):
        redirect_to = resolve_url(DEFAULT_REDIRECT)

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(username=request.POST['username'],
                                    password=request.POST['password1'])
            auth_login(request, new_user)
            return HttpResponseRedirect(redirect_to)
    else:
        form = UserCreationForm()

    return render(request, template_name, {'form': form, REDIRECT_FIELD_NAME: redirect_to})


@csrf_protect
@login_required
def profile(request, nav="profile", template_name='profile.html'):
    context = {}
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            context['success'] = True
    else:
        form = UserEditForm(instance=request.user)
    context['form'] = form
    return render(request, template_name, context)


class UserEditForm(forms.ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')


@csrf_protect
@never_cache
def login(request, template_name='users/login.html'):
    redirect_to = request.POST.get(REDIRECT_FIELD_NAME,
                                   request.GET.get(REDIRECT_FIELD_NAME, ''))

    if not is_safe_url(url=redirect_to, host=request.get_host()):
        redirect_to = resolve_url(DEFAULT_REDIRECT)

    if request.user.is_authenticated():
        return HttpResponseRedirect(redirect_to)

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return HttpResponseRedirect(redirect_to)
    else:
        form = AuthenticationForm(request)

    context = {
        'form': form,
        REDIRECT_FIELD_NAME: redirect_to
    }

    return render(request, template_name, context)


def logout(request, template_name='users/logout.html'):
    auth_logout(request)

    redirect_to = request.POST.get(REDIRECT_FIELD_NAME,
                                   request.GET.get(REDIRECT_FIELD_NAME, ''))

    if not is_safe_url(url=redirect_to, host=request.get_host()):
        redirect_to = resolve_url(DEFAULT_REDIRECT)

    return HttpResponseRedirect(redirect_to)


def _favourite_symbol(request, add, symbol):
    if not request.user.is_authenticated():
        return HttpResponseForbidden()

    investor = request.user.investor
    if add:
        investor.favourites.add(symbol)
    else:
        investor.favourites.remove(symbol)
    investor.save()
    return json_response({'success': 'that\'s what i\'m talking about'})


def favourite_stock(request, exchange, ticker):
    symbol = Symbol.objects.get(exchange__abbreviation=exchange, ticker=ticker)
    return _favourite_symbol(request, add=True, symbol=symbol)


def favourite_index(request, ticker):
    symbol = Symbol.objects.get(ticker=ticker)
    return _favourite_symbol(request, add=True, symbol=symbol)


def unfavourite_stock(request, exchange, ticker):
    symbol = Symbol.objects.get(exchange__abbreviation=exchange, ticker=ticker)
    return _favourite_symbol(request, add=False, symbol=symbol)


def unfavourite_index(request, ticker):
    symbol = Symbol.objects.get(ticker=ticker)
    return _favourite_symbol(request, add=False, symbol=symbol)


def list_favourites(request):
    if not request.user.is_authenticated():
        return HttpResponseForbidden()

    symbols = request.user.investor.favourites.all()
    return json_response([{'name': s.name, 'ticker': s.ticker, 'exchange': s.exchange.abbreviation} for s in symbols])
