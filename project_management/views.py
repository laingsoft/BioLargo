from django.views.generic import (ListView, CreateView, UpdateView, DeleteView,
    DetailView, View)
from app.mixins import (CompanyObjectsMixin, CompanyObjectCreateMixin,
    ProjectFilterMixin)
from management.mixins import ManagerTestMixin
from .models import Project, Task
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from api.serializers import SimpleTaskSerializer, SimpleUserSerializer
from django.db import Error
import json
from django.contrib.auth import get_user_model
from django.db.models import Q
import datetime
from .forms import TaskForm


class ProjectListView(ManagerTestMixin, ProjectFilterMixin,
    CompanyObjectsMixin, ListView):
    """
    Shows a list of projects. Allows a user (with permissions) to search for a
    project, add a project, edit or delete.
    """
    model = Project
    paginate_by = 20


class ProjectCreateView(ManagerTestMixin, CompanyObjectCreateMixin, CompanyObjectsMixin, CreateView):
    """
    View for creating templates.
    """
    model = Project
    fields = ('name', 'start', 'end', 'description')
    template_name = "project_management/project_create.html"
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
        task_data = SimpleTaskSerializer(tasks, many=True).data

        return JsonResponse({'data': task_data})

    def post(self, request, **kwargs):
        """
        uses TaskForm to parser post data into an object. Returns new task
        """
        form = TaskForm(json.loads(request.body), company=request.user.company)

        if not form.is_valid():
            print(form.errors)
            return HttpResponse(status=400)

        task = form.save(commit=False)
        task.project_id = kwargs.get('project')
        task.company = request.user.company
        task.save()

        return JsonResponse({'data': SimpleTaskSerializer(task).data})

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

        return JsonResponse({'data': SimpleTaskSerializer(task).data})

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

        return JsonResponse({'data': SimpleTaskSerializer(task).data})


def find_user(request):
    """
    user for autocomplete. Can find user by id and first_name, last_name or email.
    """
    if request.method == 'GET':
        search = request.GET.get('q', '')
        usr_id = request.GET.get('id', '')
        if search:
            qs = get_user_model().objects.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search) &
                Q(company=request.user.company)
                )
            return JsonResponse({'users': SimpleUserSerializer(qs, many=True).data})

        elif usr_id:
            user = get_user_model().objects.get(id=usr_id, company=request.user.company)

            return JsonResponse(SimpleUserSerializer(user).data)

        else:
            return JsonResponse({'users': SimpleUserSerializer(request.user.company.user_set.all(), many=True).data})


def find_experiment(request):
    """
    used for autocompleting experiment assignment.
    """
    if request.method == 'GET':
        q = request.GET.get('q')
        experiments = request.user.company.experiment_set.filter(friendly_name=q)


def task_complete(request, id):
    """
    For non-management users to set task to complete and link an experiment to
    task (optional). Will return updated, serialized task
    """
    if request.method == 'PUT':
        data = json.loads(request.body)
        status = data.get('status', 'N')
        task = get_object_or_404(Task, assigned=request.user, id=id)
        task.status = status
        task.related_experiment_id = data.get('related_experiment', None)

        task.save()

        return JsonResponse(SimpleTaskSerializer(task).data)


class UserTaskListView(ListView):
    """
    A view to display all tasks of a user.
    """
    model = Task
    template_name = 'project_management/task_list.html'
    def get_queryset(self):
        return json.dumps(SimpleTaskSerializer(self.request.user.tasks.all(), many=True).data)


class CalendarTaskView(ListView):
    """
    A view used for displaying all tasks from 1 one before current month.
    """

    model = Task
    template_name = "project_management/task_calendar.html"

    def get_queryset(self):
        today = datetime.date.today()
        last_month = today.month - 1 or 12  # if January, set to December.
        year = today.year if last_month != 12 else today.year - 1

        cutoff_date = datetime.date(year, last_month, 1)

        qs = self.request.user.company.task_set.filter(due_date__gte = cutoff_date)

        return json.dumps(SimpleTaskSerializer(qs, many=True).data)



