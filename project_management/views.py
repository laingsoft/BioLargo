from django.views.generic import (ListView, CreateView, UpdateView, DeleteView,
    DetailView, View)
from app.mixins import (CompanyObjectsMixin, CompanyObjectCreateMixin,
    ProjectFilterMixin)
from management.mixins import ManagerTestMixin
from .models import Project, Task
from .forms import TaskForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from api.serializers import TaskSerializer
from django.http import QueryDict
from django.db import Error
import json

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


class TaskView(View):
    """
    View used for Task CRUD operations. Takes JSON data.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, request, **kwargs):
        """
        Returns a list of all tasks of a project.
        """
        tasks = Task.objects.filter(
            company=request.user.company,
            project=kwargs.get('project')
            )

        # serialize task
        task_data = []
        for task in tasks:
            task_data.append(TaskSerializer(task).data)

        return JsonResponse({'data': task_data})

    def post(self, request, **kwargs):
        """
        uses TaskForm to parser post data into an object. Returns new task
        """
        form = TaskForm(json.loads(request.body), company=request.user.company)

        if not form.is_valid():
            return HttpResponse(status=400)

        task = form.save(commit=False)
        task.project_id = kwargs.get('project')
        task.company = request.user.company
        task.save()

        return JsonResponse({'data': TaskSerializer(task).data})

    def put(self, request, **kwargs):
        """
        updates task. Uses TaskForm to update.
        """
        params = json.loads(request.body)
        task = get_object_or_404(Task, id=kwargs.get('task_id'), project_id=kwargs.get('project'), company=request.user.company)

        form = TaskForm(params, instance=task, company=request.user.company)

        if not form.is_valid():
            return HttpResponse(status=400)

        try:
            task = form.save(commit=False)
            task.complete = bool(params.get('complete', False))
            task.save()

        except Error:
            return HttpResponse(status=500)

        return HttpResponse(status=200)

    def delete(self, request, **kwargs):
        """
        deletes Task.
        """
        print(request)
        task = get_object_or_404(Task, id=kwargs.get('task_id'), project_id=kwargs.get('project'), company=request.user.company)

        try:
            task.delete()
        except Error:
            return HttpResponse(status=500)

        return HttpResponse(status=200)
