from django.shortcuts import render
from accounts.models import User
from .forms import SettingsForm

# Create your views here.

def dashboard(request):
    '''
    Main entry point for the management part of the website. Intially this should show information like last logins,
    and allow ease of access to other services that are available on the management portion of the site
    '''
    users = User.objects.filter(company=request.user.company)
    return render(request, 'management/dashboard.html',{"users": users})

def usermgr(request):
    '''
    Allows the management to assign and create new users. This means that they can invite, delete, update, change user accounts
    '''
    return render(request, 'management/experiment.html')


def projectmgr(request):
    '''
    Allows the management to change projects as required. 
    '''
    return render(request, 'management/projects.html')

def experimentmgr(request):
    '''
    Allows the management to change experiments as required.
    '''
    return render (request, 'management/experiment.html')

def settingsmgr(request):
    '''
    Here is where settings like the metadata, at a glance settings, and the date format are set.
    '''
    if request.method == "POST":
        form = SettingsForm(request.POST)

        if form.is_valid():
            return HttpResponseRedirect('success')

    else:
        form = SettingsForm()
    return render(request, 'management/settings.html', {"form":form})
