from django.shortcuts import render, redirect
from accounts.models import User
from .forms import SettingsForm, ExperimentForm, UserChangeForm
from app.models import Template, Fields, Project, Experiment, ExperimentData
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
# from django.urls import reverse
from app.mixins import CompanyObjectCreateMixin, CompanyObjectsMixin
from json import loads
from django.http import HttpResponse, HttpResponseRedirect
from django.db.utils import Error
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin



# Create your views here.
class ManagerTestMixin(UserPassesTestMixin):
    """
    mixin used to limit access to managers and admin only.
    """
    def test_func(self):
        return self.request.user.is_manager or self.user.is_admin


def dashboard(request):
    '''
    Main entry point for the management part of the website. Intially this should show information like last logins,
    and allow ease of access to other services that are available on the management portion of the site
    '''
    users = User.objects.filter(company=request.user.company)
    return render(request, 'management/dashboard.html',{"users": users})

# def usermgr(request):
#     '''
#     Allows the management to assign and create new users. This means that they can invite, delete, update, change user accounts
#     '''
#     return render(request, 'management/experiment.html')


class ProjectListView(ManagerTestMixin, CompanyObjectsMixin, ListView):
    model = Project
    template_name = "management/projects.html"
    paginate_by = 20


class ProjectCreateView(ManagerTestMixin, CompanyObjectCreateMixin, CompanyObjectsMixin, CreateView):
    """
    View for creating templates.
    """
    model = Project
    fields = ('name', 'start', 'end', 'description')
    template_name = "management/project_update.html"
    success_url = "/management/projects"


class ProjectUpdateView(ManagerTestMixin, CompanyObjectsMixin, UpdateView):
    model = Project
    fields = ("name", "start", "end", "description")
    template_name = "management/project_update.html"
    success_url = "/management/projects"


class ProjectDeleteView(ManagerTestMixin, CompanyObjectsMixin, DeleteView):
    """
    View for deleting template.
    """
    model = Project
    template_name = "management/template_confirm_delete.html"
    success_url = "/management/projects"


class ExperimentListView(ManagerTestMixin, CompanyObjectsMixin, ListView):
    model = Experiment
    template_name = "management/experiment_list.html"
    paginate_by = 20


class ExperimentUpdateView(ManagerTestMixin, CompanyObjectsMixin, UpdateView):
    model = Experiment
    template_name = "management/experiment_update.html"
    success_url = "/management/experiments"
    # fields = ('friendly_name', 'metadata', 'tags', 'project')
    form_class = ExperimentForm

    def get_context_data(self, **kwargs):
        """
        returns ExperimentData objects of Experiment and headers for experiment
        data along with default context.
        """
        context = super().get_context_data(**kwargs)
        context["exp_data"] = ExperimentData.objects.filter(experiment=self.kwargs['pk'], company=self.request.user.company)

        # TODO: require SOME data to be added on upload.

        try:
            context["headers"] = list(context["exp_data"][0].experimentData.keys())
        except IndexError:
            context["headers"] = [' ']
            context["exp_data"] = [[' ']]

        return context

    def form_valid(self, form):
        """
        handles exp_data json experiment form.
        TODO: add data type checking for fields.
        """
        exp_data = self.request.POST.get("exp_data")

        try:
            exp_data = loads(exp_data)
        except ValueError:
            return HttpResponse("Invalid Data", status="400")

        exp_data = [x for x in exp_data if any(x.values())]
        if not exp_data:
            return HttpResponse("No experiment data found.", status="400")

        self.object = form.save()

        ExperimentData.objects.filter(experiment=self.kwargs['pk'], company=self.request.user.company).delete()

        try:
            data_objects = []
            for item in exp_data:
                data_objects.append(ExperimentData(company=self.request.user.company, experimentData=item, experiment=self.object))

            ExperimentData.objects.bulk_create(data_objects)

        except Error:  # a generic database error
            return HttpResponse(status=500)

        return redirect(self.get_success_url())


class ExperimentDeleteView(ManagerTestMixin, CompanyObjectsMixin, DeleteView):
    model = Experiment
    success_url = "/management/experiments"
    template_name = "management/template_confirm_delete.html"


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


class TemplateListView(ManagerTestMixin, CompanyObjectsMixin, ListView):
    """
    Class based view for displaying a list of templates.
    """
    model = Template
    template_name = "management/template_list.html"
    paginate_by = 20


class TemplateCreateView(ManagerTestMixin, CompanyObjectCreateMixin, CompanyObjectsMixin, CreateView):
    """
    View for creating templates.
    """
    model = Template
    fields = ('name', 'fields', 'metadata')
    template_name = "management/template_form.html"
    success_url = "/management/templates"


class TemplateUpdateView(ManagerTestMixin, CompanyObjectsMixin, UpdateView):
    """
    View for editing templates.
    """
    model = Template
    fields = ('name', 'fields', 'metadata')
    template_name = "management/template_form.html"
    success_url = "/management/templates"


class TemplateDeleteView(ManagerTestMixin, CompanyObjectsMixin, DeleteView):
    """
    View for deleting template.
    """
    model = Template
    template_name = "management/template_confirm_delete.html"
    success_url = "/management/templates"


class FieldListView(ManagerTestMixin, CompanyObjectsMixin, ListView):
    """
    Displays a list of fields.
    """
    model = Fields
    paginate_by = 20
    template_name = "management/fields_list.html"


class FieldCreateView(ManagerTestMixin, CompanyObjectCreateMixin, CompanyObjectsMixin, CreateView):
    """
    Displays a list of fields.
    """
    model = Fields
    fields = ('name', 'data_type', 'empty')
    template_name = "management/fields_form.html"
    success_url = "/management/fields"


class FieldUpdateView(ManagerTestMixin, CompanyObjectsMixin, UpdateView):
    """
    View for editing fields.
    """
    model = Fields
    fields = ('name', 'data_type', 'empty')
    template_name = "management/fields_form.html"
    success_url = "/management/fields"


class FieldDeleteView(ManagerTestMixin, CompanyObjectsMixin, DeleteView):
    """
    View for editing fields.
    """
    model = Fields
    template_name = "management/fields_delete.html"
    success_url = "/management/fields"


class UserListview(ManagerTestMixin, CompanyObjectsMixin, ListView):
    """
    displays a list of users. Users can be found by first name, last name
    and email.
    """
    model = get_user_model()
    template_name = "management/user_list.html"
    paginate_by = 20


class UserUpdateView(ManagerTestMixin, CompanyObjectsMixin, UpdateView):
    model = get_user_model()
    template_name = "management/user_update.html"
    # fields = ("first_name", "last_name", "email", "password", "groups", "user_permissions" )
    form_class = UserChangeForm
    success_url = "/management/users"
