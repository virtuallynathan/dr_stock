from django import forms
from django.conf import settings
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, resolve_url
from django.core.mail import EmailMessage
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.utils.http import is_safe_url


REDIRECT_FIELD_NAME = 'next'


@csrf_protect
@never_cache
def register(request, template_name='register.html'):
    redirect_to = request.POST.get(REDIRECT_FIELD_NAME,
                                   request.GET.get(REDIRECT_FIELD_NAME, ''));

    if not is_safe_url(url=redirect_to, host=request.get_host()):
        redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

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
def profile(request, template_name='profile.html'):
    if request.method == 'POST': # If the form has been submitted...
        form = UserEditForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            form.save()
            return HttpResponseRedirect('/accounts/profile') # Redirect after POST
    return render(request, template_name)

class UserEditForm(forms.Form):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)



# Send an email from form
def send_email(request):
    errors = []
    if request.method == 'POST':
        if not request.POST.get('subject', ''):
            errors.append('Enter a subject.')
        if not request.POST.get('message', ''):
            errors.append('Enter a message.')
        if request.POST.get('email') and '@' not in request.POST['email']:
            errors.append('Enter a valid e-mail address.')
        if not errors:
            send_mail(
                request.POST['subject'],
                request.POST['message'],
                request.POST.get('email', 'jamesspyt@gmail.com'),
                ['jamesspyt@gmail.com'],
            )
            return HttpResponseRedirect(request, '/accounts/sent')
    return render(request, 'email.html', {'errors': errors})

def sent(request, template_name='sent.html'):
    return render(request, template_name)


@csrf_protect
@never_cache
def login(request, template_name='users/login.html'):
    redirect_to = request.POST.get(REDIRECT_FIELD_NAME,
                                   request.GET.get(REDIRECT_FIELD_NAME, ''))

    if not is_safe_url(url=redirect_to, host=request.get_host()):
        redirect_to = resolve_url(redirect_to)

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
        redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

    return HttpResponseRedirect(redirect_to)

