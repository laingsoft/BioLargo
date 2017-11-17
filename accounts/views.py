from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import get_user
from django.contrib.auth.models import User
from .models import Scientist
from .forms import profileForm
# Create your views here.

def register(request):
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password) 
                scientist = Scientist(user=user)
                scientist.save()
                auth_login(request, user)
                print("got here")
                return HttpResponseRedirect('/app')
            else:
                HttpResponseRedirect('/accounts/login')
                
        else:
            form = UserCreationForm()
            login_form = AuthenticationForm()
            return render(request, 'accounts/login.html', {'form':form, 'login_form':login_form})

#  using default one for now.
# def login(request):
#     if request.method == "POST":
#         form = AuthenticationForm(data = request.POST)

#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password') 
#             user = authenticate(username=username, password=raw_password) 
#             auth_login(request,user)
#             return HttpResponseRedirect('/app')
#         else:
#             return HttpResponseRedirect('/accounts/login')



#     else:
#         form = UserCreationForm()
#         login_form = AuthenticationForm()
#         return render(request, 'accounts/login.html', {'form':form, 'login_form':login_form})

def userpage(request, usr_id):
        view_user = User.objects.get(id=usr_id)
        return render(request, 'accounts/user.html',{'userdata':view_user, 'usr':get_user(request)})


def profile(request):
        if request.method == "POST":
                form = profileForm(data=request.POST, instance = request.user)
                if form.is_valid():
                        form.save()
                        return redirect("/accounts/profile/")
        else:
                form = profileForm(instance = request.user)
                return render(request, 'accounts/profile.html',{'userdata':Scientist.objects.get(user=get_user(request)), 'usr':get_user(request), "form":form})



def userlist(request):
        usr = get_user(request)
        usrlist = User.objects.all()

        return render(request, 'accounts/users.html', {'user_list':usrlist , 'usr':usr})

def messaging(request):
        usr = get_user(request)
        return render(request, 'accounts/messages.html', {'usr':usr})
