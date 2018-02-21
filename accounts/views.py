from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from django.contrib.auth import get_user, get_user_model
from .forms import profileForm, CompanyForm, UserForm
from django.http import Http404
from .models import Invite, Plan
from django.db import IntegrityError
from secrets import token_urlsafe
# Create your views here.


def register_user(request, linkHash):
    """
    View used to register a new user within a company
    """
    try:
        invite = Invite.objects.get(hash=linkHash)
        company = invite.company
    except Invite.DoesNotExist:
        raise Http404

    if request.method == "GET":
        user_form = UserForm()
        if invite.validate:
            return render(request, 'registration/register.html',
                {"form": user_form, "company": company})
        else:
            
            raise Http404

    if request.method == "POST":
        form = UserForm(request.POST)
        print(form)
        if form.is_valid():

            try:
                user = form.save(commit=False)
                user.company = company
                user.save()

            except IntegrityError:
                raise HttpResponse("Error creating user. Please try again later.", status=500)

            auth_login(request, user)

            return redirect("/app")


def company_register(request):
    """
    View used to register a new user and company.
    Registers a new user with is_admin and is_management set to true.
    """

    if request.method == "GET":

        # For testing. Remove this line later!
        if not Plan.objects.all().exists():
            Plan.objects.create(name="Test Plan", price=0)

        plan = request.GET.get('p')

        company_form = CompanyForm(initial = {'plan': plan }, prefix="company")
        user_form = UserForm(prefix = "user")

    if request.method == "POST":
        company_form = CompanyForm(request.POST, prefix="company")
        user_form = UserForm(request.POST, prefix="user")

        if company_form.is_valid() and user_form.is_valid():

            company = company_form.save()

            try:
                user = user_form.save(commit=False)
                user.company = company
                user.is_admin = True
                user.is_manager = True
                user.save()

            except IntegrityError:
                return HttpResponse("Error creating company.\
                 Please try again later.", status=500)

            auth_login(request, user)
            return redirect("/app")

    context = {
        "company_form": company_form,
        "user_form": user_form
    }

    return render(request, 'registration/company_registration.html', context)


def userpage(request, usr_id):
    '''
    Generates the page for each user. This is the view of the request user
    looking at another user. The fields returned
    Should not be editable.
    '''
    company = request.user.company
    view_user = get_user_model().objects.get(id=usr_id)

    if view_user.company != company:
        return Http404("User not found")

    return render(request, 'accounts/user.html', {'userdata': view_user,
        'usr':get_user(request)})


def profile(request):
    '''
    Generates the profile for the requesting user. All of the fields here
    should be editable
    '''
    if request.method == "POST":
        form = profileForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("/accounts/profile/")
    else:
        form = profileForm(instance=request.user)

        context = {
            'userdata': request.user,
            "form": form
        }

    return render(request, 'accounts/profile.html', context)



def userlist(request):
    '''
    Returns the page that lists all of the users within the requesting user's company.
    '''
    company = request.user.company
    usrlist = get_user_model().objects.filter(company=company)

    return render(request, 'accounts/users.html', {'user_list':usrlist})

def messaging(request):
    '''
    Should eventually have messaging functionality.
    '''
    usr = get_user(request)
    return render(request, 'accounts/messages.html', {'usr':usr})


def generate_invite(request):
    this_user = request.user
    this_company = this_user.company
    try:
        openInvite = Invite.objects.get(company=this_company)
        token = openInvite.hash

    except Invite.DoesNotExist:
        #create a new invite
        invite = Invite()
        invite.hash = token_urlsafe(32)
        invite.company = this_user.company
        invite.save()
        token = invite.hash
        #return the url

    return JsonResponse({"token":token})
