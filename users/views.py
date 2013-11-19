from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.mail import EmailMessage

def register(request, template_name='register.html'):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(username=request.POST['username'],
                                    password=request.POST['password1'])
            login(request, new_user)
            return HttpResponseRedirect('/home/')
    else:
        form = UserCreationForm()
    return render(request, template_name, {'form': form})

@login_required
def profile(request, template_name='home.html'):
    return render(request, template_name)

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