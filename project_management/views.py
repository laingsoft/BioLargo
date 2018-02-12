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
from django.db import Error
import json
from django.contrib.auth import get_user_model
from django.db.models import Q

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
    success_url = "/management/projects"


class ProjectDeleteView(ManagerTestMixin, CompanyObjectsMixin, DeleteView):
    """
    View for deleting template.
    """
    model = Project
    template_name = "management/template_confirm_delete.html"
    success_url = "/management/projects"


class TaskView(ManagerTestMixin, View):
    """
    View used for Task CRUD operations. Takes JSON data. Management staff only.
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
        task_data = TaskSerializer(tasks, many=True).data

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

        return JsonResponse({'data': TaskSerializer(task).data})

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

        return JsonResponse({'data': TaskSerializer(task).data})


def find_user(request):
    if request.method == 'GET':
        search = request.GET.get('q', '')
        qs = get_user_model().objects.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search) &
            Q(company=request.user.company)
            ).values('id', 'first_name', 'last_name', 'email')


        return JsonResponse({'users': list(qs)})


def task_complete(request, id):
    """
    For non-management users to set task to complete and link an experiment to
    task (optional). Will return updated, serialized task (because backbone)
    """
    if request.method == 'PUT':
        data = json.loads(request.body)
        complete = bool(data.get('complete', False))
        task = get_object_or_404(Task, assigned=request.user, id=id)
        task.complete = complete
        task.related_experiment_id = data.get('related_experiment', None)

        task.save()

        return JsonResponse(TaskSerializer(task).data)


class UserTaskListView(ListView):
    """
    A view to display all tasks of a user.
    """
    model = Task
    template_name = 'project_management/task_list.html'
    def get_queryset(self):
        return json.dumps(TaskSerializer(self.request.user.tasks.all(), many=True).data)
        return self.request.user.tasks.all()
