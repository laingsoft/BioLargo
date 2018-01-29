from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Project
from app.mixins import CompanyObjectsMixin, CompanyObjectCreateMixin
from app.mixins import ProjectFilterMixin
from management.mixins import ManagerTestMixin


class ProjectListView(ManagerTestMixin, ProjectFilterMixin,
    CompanyObjectsMixin, ListView):
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
