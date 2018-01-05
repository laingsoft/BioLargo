from django.shortcuts import render, redirect
from accounts.models import User
from .forms import SettingsForm
from app.models import Template, Fields, Project, Experiment, ExperimentData
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
# from django.urls import reverse
from app.mixins import CompanyObjectCreateMixin, CompanyObjectsMixin
from json import loads
from django.http import HttpResponseBadRequest, HttpResponseRedirect
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


class ProjectListView(CompanyObjectsMixin, ListView):
    model = Project
    template_name = "management/projects.html"
    paginate_by = 20


class ProjectCreateView(CompanyObjectCreateMixin, CompanyObjectsMixin, CreateView):
    """
    View for creating templates.
    """
    model = Project
    fields = ('name', 'start', 'end', 'description')
    template_name = "management/project_update.html"
    success_url = "/management/projects"


class ProjectUpdateView(CompanyObjectsMixin, UpdateView):
    model = Project
    fields = ("name", "start", "end", "description")
    template_name = "management/project_update.html"
    success_url = "/management/projects"


class ProjectDeleteView(CompanyObjectsMixin, DeleteView):
    """
    View for deleting template.
    """
    model = Project
    template_name = "management/template_confirm_delete.html"
    success_url = "/management/projects"


class ExperimentListView(CompanyObjectsMixin, ListView):
    model = Experiment
    template_name = "management/experiment_list.html"
    paginate_by = 20


class ExperimentUpdateView(CompanyObjectsMixin, UpdateView):
    model = Experiment
    template_name = "management/experiment_update.html"
    success_url = "/management/experiments"
    fields = ('friendly_name', 'metadata', 'tags', 'project')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["exp_data"] = ExperimentData.objects.filter(experiment=self.kwargs['pk'], company=self.request.user.company)
        try:  # remove this try except and require some data to be added.
            context["headers"] = list(context["exp_data"][0].experimentData.keys())
        except IndexError:
            pass

        return context

    def form_valid(self, form):
        # parse the json & validate
        exp_data = self.request.POST.get("exp_data")

        try:
            exp_data = loads(exp_data)
        except ValueError:
            return HttpResponseBadRequest("Invalid Data")

        # save Experiment
        self.object = form.save()

        # delete old data
        ExperimentData.objects.filter(experiment=self.kwargs['pk'], company=self.request.user.company).delete()

        # Create with Experiment
        data_objects = []
        for item in exp_data:
            data_objects.append(ExperimentData(experimentData=item, experiment=self.object))

        # save ExperimentData objects
        ExperimentData.objects.bulk_create(data_objects)

        return redirect(self.get_success_url())


def settingsmgr(request):
    '''
    Here is where settings like the metadata, at a glance settings, and the
    date format are set.
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
    template_name = "management/template_confirm_delete.html"
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
