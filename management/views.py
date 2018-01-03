from django.shortcuts import render, redirect
from accounts.models import User
from .forms import SettingsForm
from app.models import Template, Fields
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
# from django.urls import reverse
from django.views.generic.detail import SingleObjectMixin
from app.mixins import CompanyObjectCreateMixin, CompanyObjectsMixin
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
    return render(request, 'management/settings.html', {"form": form})


class TemplateListView(CompanyObjectsMixin, ListView):
    """
    Class based view for displaying a list of templates.
    """
    model = Template
    template_name = "management/template_list.html"
    paginate_by = 20


class TemplateCreateView(CompanyObjectCreateMixin, CompanyObjectsMixin, CreateView):
    """
    View for creating templates.
    """
    model = Template
    fields = ('name', 'fields', 'metadata')
    template_name = "management/template_form.html"
    success_url = "/management/templates"


class TemplateUpdateView(CompanyObjectsMixin, UpdateView):
    """
    View for editing templates.
    """
    model = Template
    fields = ('name', 'fields', 'metadata')
    template_name = "management/template_form.html"
    success_url = "/management/templates"


class TemplateDeleteView(CompanyObjectsMixin, DeleteView):
    """
    View for deleting template.
    """
    model = Template
    template_name = "management/template_delete.html"
    success_url = "/management/templates"


class FieldListView(CompanyObjectsMixin, ListView):
    """
    Displays a list of fields.
    """
    model = Fields
    paginate_by = 20
    template_name = "management/fields_list.html"


class FieldCreateView(CompanyObjectCreateMixin, CompanyObjectsMixin, CreateView):
    """
    Displays a list of fields.
    """
    model = Fields
    fields = ('name', 'data_type', 'empty')
    template_name = "management/fields_form.html"
    success_url = "/management/fields"


class FieldUpdateView(CompanyObjectsMixin, UpdateView):
    """
    View for editing fields.
    """
    model = Fields
    fields = ('name', 'data_type', 'empty')
    template_name = "management/fields_form.html"
    success_url = "/management/fields"


class FieldDeleteView(CompanyObjectsMixin, DeleteView):
    """
    View for editing fields.
    """
    model = Fields
    template_name = "management/fields_delete.html"
    success_url = "/management/fields"
