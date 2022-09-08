from django.shortcuts import render
from . import forms

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from . import models

# Create your views here.
def profile(request):
    diction = {

    }
    if request.user.is_authenticated:
        current_user = request.user
        user_id = current_user.id

        user_info = User.objects.get(pk=user_id)
        user_more_info = models.UserInfo.objects.get(user__pk=user_id)

        diction = {
            'user_info': user_info,
            'user_more_info': user_more_info,
        }

    return render(request, 'index/index.html', context=diction)

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = forms.UserForm(data=request.POST)
        user_info_form = forms.UserInfoForm(data=request.POST)

        if user_form.is_valid() and user_info_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            user_info = user_info_form.save(commit=False)
            user_info.user = user

            if 'profile_pic' in request.FILES:
                user_info.profile_pic = request.FILES['profile_pic']
            
            user_info.save()
            registered = True
    else:
        user_form = forms.UserForm()
        user_info_form = forms.UserInfoForm()
    diction = {
        'user_form': user_form,
        'user_info_form': user_info_form,
        'registered': registered,
    }
    return render(request, 'login/register.html', context=diction)

def login_form(request):
    diction = {}
    return render(request, 'login/login.html', context=diction)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password = password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index:profile'))
            else:
                return HttpResponse('Your account is not active!')
        else:
            return HttpResponse('Your info is not correct')
    else:
        return HttpResponseRedirect(reverse('index:profile'))

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index:login'))