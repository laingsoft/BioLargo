from django.views.generic import (ListView, CreateView, UpdateView, DeleteView,
    DetailView)
from app.mixins import (CompanyObjectsMixin, CompanyObjectCreateMixin,
    ProjectFilterMixin)
from management.mixins import ManagerTestMixin
from .models import Project, Task
from .forms import TaskForm
from django.http import HttpResponse, JsonResponse


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


class ProjectDetailView(CompanyObjectsMixin, DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form'] = TaskForm(company=self.request.user.company)
        return context


def tasks(request, project):
    """
    on get gets a list of tasks related to project.
    on post creates a new tasl
    """
    if not Project.objects.filter(id=project, company=request.user.company).exists():
        return HttpResponse(status=400)

    if request.method == 'POST':
        form = TaskForm(request.POST, company=request.user.company)

        if form.is_valid():
            task = form.save(commit=False)
            task.company = request.user.company
            task.project_id = project
            task.save()

            return HttpResponse(status=201)
        return HttpResponse(status=400)

    if request.method == 'GET':
        return JsonResponse({x.id: x.name for x in Task.incomplete.filter(project=project)})

