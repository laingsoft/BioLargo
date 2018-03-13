from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from .parsers import Parser, JsonParser
from .models import Experiment, ExperimentData, Template, Fields, Comment
from .models import Tag, Notification
from project_management.models import Project
from io import TextIOWrapper
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user, get_user_model
from django.db.models import Count
from django.db.models.functions import TruncDay
import json
import csv
from .forms import FileUpload, ExperimentForm, ExperimentDataForm, ProjectForm
from io import StringIO
from django.views.generic import ListView, DetailView
from .mixins import CompanyObjectsMixin, ExpFilterMixin, ProjectFilterMixin
import datetime
from project_management.models import Task


@login_required
def index(request):
    """
    Index should be the main landing page for the application. It will show
    all of the available data to the researcher, and allow them to link to
    other resources, such as uploading and analysis.
    """

    company = request.user.company

    latest = Experiment.objects.filter(company=company).order_by('-id')[:10]

    return render(request, 'app/index.html', {'latest': latest})


@login_required
def upload(request):
    """
    View for uploading data through form or upload file.
    Will accept any file format supported by the parser.
    The form itself sends experiment data and metadata as JSON.

    """
    company = request.user.company

    if request.method == "POST":
        exp_form = ExperimentForm(request.POST, prefix='exp', company=company)
        file_form = FileUpload(request.POST, request.FILES, prefix='file')
        exp_data = ExperimentDataForm(request.POST, prefix='exp_data', company=company)

        print("request", request)

        if exp_form.is_valid() and (file_form.is_valid() or exp_data.is_valid()):
            print("exp_form cleaned_data", exp_form.cleaned_data)


            # get experiment object and add missing attributes.
            # still missing metadata.

            experiment = exp_form.save(commit=False)
            experiment.company = company
            experiment.user = request.user

            # if it was a file upload, parse and populate form with data for
            # confirmation.
            if file_form.is_valid():
                parser = Parser(buffer=TextIOWrapper(
                    request.FILES['file-upload_file'],
                    encoding=request.encoding
                    ))
                parser.get_parser().create_objects(experiment)

            # if it was a form upload
            elif exp_data.is_valid():
                data = exp_data.cleaned_data.get("json")
                parser = JsonParser(buffer=StringIO(data))
                parser.create_objects(experiment)

            exp_form.save_m2m()

            return redirect("/app/upload/success/" + str(experiment.id))

    if request.method == "GET":
        exp_form = ExperimentForm(prefix='exp', company=company)
        file_form = FileUpload(prefix='file')
        exp_data = ExperimentDataForm(prefix='exp_data', company=company)

    # to handle errors, the context declaration is here.
    context = {
        'exp_form': exp_form,
        'file_form': file_form,
        'exp_data': exp_data
    }

    return render(request, 'app/upload.html', context)


@login_required
def get_template(request):
    """
    Responds to ajax request for getting fields in template.
    """
    if request.method == 'GET':

        template = get_object_or_404(
            Template,
            company=request.user.company,
            name=request.GET.get('name'))

        metadata = list(template.metadata.values_list('name', 'data_type'))
        fields = list(template.fields.values_list('name', 'data_type'))

        context = {
            "metadata": metadata,
            "fields": fields,
        }

        return JsonResponse(context)

    raise Http404


# Response for successful upload.
@login_required
def upload_success(request, exp_id):
    get_object_or_404(Experiment, id=exp_id)
    return render(request, 'app/upload_success.html', {'exp_id': exp_id})


class ExperimentListView(ExpFilterMixin, CompanyObjectsMixin, ListView):
    """
    View for Experiment list
    """
    model = Experiment
    template_name = 'app/experiments_page.html'


class ExperimentDetailView(CompanyObjectsMixin, DetailView):
    model = Experiment
    template_name = "app/experiment.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['metadata'] = self.object.metadata
        context['comments'] = Comment.objects.filter(experiment=self.object)
        context['watched'] = self.object.followers.filter(pk=self.request.user.pk).exists()

        return context

@login_required
def experiment_json(request, exp_id):
    company = request.user.company
    data = ExperimentData.objects.filter(company=company, experiment=exp_id)

    if not data.exists():
        raise Http404("Experiment does not exist.")

    newval = {}
    newval = {k: v.experimentData for k, v in enumerate(data)}
    return JsonResponse(newval)

@login_required
def experimentrm(request, exp_id):
    company = request.user.company
    data = Experiment.objects.filter(company=company, id=exp_id)
    if not data.exists():
        raise Http404("Experiment does not exist.")

    res = data.delete()
    return JsonResponse({"result": res[0]>0})


@login_required
def get_csv(request, exp_id, header=0):
    company = request.user.company
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="'+exp_id+'.csv"'
    vals = ExperimentData.objects.filter(company=company, experiment=exp_id)
    newdata = []
    [newdata.append(json.loads(i.experimentData)) for i in vals]
    fieldnames = []
    [fieldnames.append(k) for k in newdata[0]]
    writer = csv.DictWriter(response, fieldnames)
    writer.writeheader()
    [writer.writerow(i) for i in newdata]
    return response


class ProjectListView(ProjectFilterMixin, CompanyObjectsMixin, ListView):
    model = Project
    template_name = 'app/project_list.html'


class ProjectDetailView(CompanyObjectsMixin, DetailView):
    model = Project
    template_name = "app/view_project.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['experiments'] = self.object.experiment_set.all()
        context['user_count'] = context['experiments'].distinct("user").count()
        context['watched'] = self.object.followers.filter(pk=self.request.user.pk).exists()
        return context

@login_required
def create_tag(request):
    if request.method == "POST":
        tag = request.POST.get("tag")
        Tag.objects.create(name=tag, company=request.user.company)

        return HttpResponse(status=201)

    raise Http404


@login_required
def watch(request):
    """
    View for watching Experiments and Projects
    """
    OBJ = {
        'EXP': Experiment,
        'PRJ': Project
        }

    if request.method == "POST":
        pk = request.POST.get("pk")
        t = request.POST.get("type")

        if OBJ[t].objects.filter(pk=pk).exists():
            obj = OBJ[t].objects.get(pk=pk)

            if obj.followers.filter(pk=request.user.pk).exists():
                obj.followers.remove(request.user)

            else:
                obj.followers.add(request.user)

            return JsonResponse({'success': True})

        return JsonResponse({'success': False})


class WatchedExperimentListView(ListView):
    """
    List of watched experiments.
    TODO: make less ugly
    """
    model = Experiment
    template_name = "app/experiments_page.html"

    def get_queryset(self):
        return self.request.user.followed_experiments.all()


class WatchedProjectsListView(ListView):
    model = Project
    template_name = "app/project_list.html"

    def get_queryset(self):
        return self.request.user.followed_project.all()


def notif_read(request):
    if request.method == "POST":
        pk = int(request.POST["pk"])
        n = Notification.unread.get(pk=pk, recipient=request.user)
        n.read = True
        n.save()
        return JsonResponse({'success': True})



