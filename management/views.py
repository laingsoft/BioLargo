from django.shortcuts import render, redirect
from accounts.models import User
from .forms import SettingsForm, ExperimentForm, UserChangeForm, GroupForm
from .models import Settings
from app.models import Template, Fields, Project, Experiment, ExperimentData
from accounts.models import Company
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from app.mixins import CompanyObjectCreateMixin, CompanyObjectsMixin
from json import loads
from django.http import HttpResponse, HttpResponseRedirect
from django.db.utils import Error
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.views import View
from app.mixins import ExpFilterMixin, ProjectFilterMixin, BaseFilterMixin, UserFilterMixin
from django.contrib.auth.models import Group

# Create your views here.


class ManagerTestMixin(UserPassesTestMixin):
    """
    mixin used to limit access to managers and admin only. To check for
    class based permissions, add test_func method to view with condition.
    """
    login_url = "/management/login"

    def test_func(self):
        return self.request.user.is_authenticated and (self.request.user.is_manager or self.request.user.is_admin)


class Dashboard(ManagerTestMixin, View):
    """
    Main entry point for the management part of the website. Intially this
    should show information like last logins,and allow ease of access to other
    services that are available on the management portion of the site.
    """
    def get(self, request):
        users = User.objects.filter(company=request.user.company)
        return render(request, 'management/dashboard.html', {"users": users})


class ProjectListView(ManagerTestMixin, ProjectFilterMixin, CompanyObjectsMixin, ListView):
    """
    Shows a list of projects. Allows a user (with permissions) to search for a
    project, add a project, edit or delete.
    """
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
    """
    View used for updaing an existing project.
    """
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


class ExperimentListView(ManagerTestMixin, ExpFilterMixin, CompanyObjectsMixin, ListView):
    """
    Lists Experiments within a company, if user has permissions to page.
    """
    model = Experiment
    template_name = "management/experiment_list.html"
    paginate_by = 20


class ExperimentUpdateView(ManagerTestMixin, CompanyObjectsMixin, UpdateView):
    """
    View for editing experiments through the management panel.
    """
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
    """
    confirms the delete request on get and deletes on post
    """
    model = Experiment
    success_url = "/management/experiments"
    template_name = "management/template_confirm_delete.html"


class SettingsUpdateView(UpdateView):
    """
    View for editing settings and company information.
    Overrides methods from mixins and parent class to accomodate the extra
    settings modelform.
    """
    fields = ('name', 'address', 'phone')
    model = Company
    template_name = "management/settings.html"
    success_url = "/management/settings"

    def get_object(self, **kwargs):
        """
        returns the request user's company.
        """
        return self.request.user.company

    def get_context_data(self, **kwargs):
        """
        creates the settings form. Will create new settings object if one
        doesn't already exist.
        """

        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
            settings = Settings.objects.get_or_create(company = self.object)
            kwargs['settings'] = SettingsForm(instance=settings[0], prefix="settings")

        return super().get_context_data(**kwargs)

    def form_valid(self, form, settings):
        """
        handles model saving for company and settings.
        """

        settings.save()
        self.object = form.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, settings):
        """
        if invalid, returns both forms.
        """
        return self.render_to_response(self.get_context_data(form=form, settings=settings))

    def post(self, request):
        """
        overriden to validate two both company and settings forms.
        """
        self.object = self.get_object()

        form = self.get_form()
        settings_instance = Settings.objects.get(company=self.object)
        settings = SettingsForm(self.request.POST, prefix="settings", instance=settings_instance)

        if form.is_valid() and settings.is_valid():
            return self.form_valid(form, settings)

        else:
            return self.form_invalid(form, settings)


class TemplateListView(ManagerTestMixin, BaseFilterMixin, CompanyObjectsMixin, ListView):
    """
    Class based view for displaying a list of templates.
    """
    model = Template
    template_name = "management/template_list.html"
    paginate_by = 20

    FILTERS = {
        "name": lambda x: ("name__icontains", x[0])
    }

    ORDER_FIELDS = (
        "name",
    )



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


class FieldListView(ManagerTestMixin, BaseFilterMixin, CompanyObjectsMixin, ListView):
    """
    Displays a list of fields.
    """
    model = Fields
    paginate_by = 20
    template_name = "management/fields_list.html"
    FILTERS = {
        "name": lambda x: ("name__icontains", x[0]),
        "data_type" : lambda x: ("data_type", x[0])
    }

    ORDER_FIELDS = (
        "name",
        "data_type"
    )


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


class UserListview(ManagerTestMixin, UserFilterMixin, CompanyObjectsMixin, ListView):
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


class UserGroupListView(BaseFilterMixin, ListView):
    """
    Displays a list of user groups.
    """
    model = Group
    template_name = "management/groups_list.html"
    paginate_by = 20

    FILTERS = {
        "name": lambda x: ("name__icontains", x[0]),
        "description": lambda x: ("extra__description__icontains", x[0]),
    }

    ORDER_FIELDS = (
        "name",
    )

    def get_queryset(self):
        """
        Gets queryset of groups for specified company. Slightly different field
        so it doesn't use the CompanyObjectsMixin.
        """
        qs = super().get_queryset()
        qs = qs.filter(extra__company=self.request.user.company)

        return qs


class UserGroupCreateView(CreateView):
    """
    Displays form for creating new user group.
    """
    model = Group
    template_name = "management/groups_form.html"
    form_class = GroupForm
    success_url = '/management/groups'

    def form_valid(self, form):
        """
        handles valid form. Overriden to add company argument to form
        """
        self.object = form.save(company=self.request.user.company)
        return HttpResponseRedirect(self.get_success_url())


class UserGroupUpdateView(UpdateView):
    """
    Updates an existing group. contains some copy-paste code
    from the two previous views.
    """
    model = Group
    template_name = "management/groups_form.html"
    form_class = GroupForm
    success_url = '/management/groups'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(extra__company=self.request.user.company)
        return qs

    def form_valid(self, form):
        """
        handles valid form.
        """
        self.object = form.save(company=self.request.user.company)
        return HttpResponseRedirect(self.get_success_url())


class UserGroupDeleteView(DeleteView):
    model = Group
    template_name = 'management/template_confirm_delete.html'
    success_url = '/management/groups'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(extra__company=self.request.user.company)
        return qs


class ManagementLoginView(LoginView):
    """
    a log in view to (hopefully) fix the redirect loop
    """
    template_name = "admin/login.html"

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated and (user.is_manager or user.is_manager):
            redirect_to = self.get_success_url()

            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )

            return HttpResponseRedirect(redirect_to)

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        url = self.get_redirect_url()
        return url
