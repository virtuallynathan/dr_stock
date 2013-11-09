from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render

def register(request, template_name='register.html'):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(username=request.POST['username'],
                                    password=request.POST['password1'])
            login(request, new_user)
            return HttpResponseRedirect('/accounts/profile')
    else:
        form = UserCreationForm()
    return render(request, template_name, {'form': form})

@login_required
def profile(request, template_name='profile.html'):
    return render(request, template_name)
