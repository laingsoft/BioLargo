from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import get_user
from django.contrib.auth.models import User
# Create your views here.

def register(request):
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                auth_login(request, user)
                return redirect('/app')
        else:
            form = UserCreationForm()
            login_form = AuthenticationForm()
            return render(request, 'accounts/login.html', {'form':form, 'login_form':login_form})


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            auth_login(request,user)
            return HttpResponseRedirect('/app')
        else:
            return HttpResponseRedirect('/accounts/login')



    else:
        form = UserCreationForm()
        login_form = AuthenticationForm()
        return render(request, 'accounts/login.html', {'form':form, 'login_form':login_form})

def userpage(request, usr_id):
        return render(request, 'accounts/user.html',{'userdata':User.objects.values_list()})
