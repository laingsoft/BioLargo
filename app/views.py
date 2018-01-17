from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from .parsers import Parser, JsonParser
from .models import Experiment, ExperimentData, Template, Fields, Comment
from .models import Project, Tag
from io import TextIOWrapper
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
from django.db.models import Count
from django.db.models.functions import TruncDay
import json
import csv
from .forms import FileUpload, ExperimentForm, ExperimentDataForm, ProjectForm
from io import StringIO
from django.views.generic import ListView
from .mixins import CompanyObjectsMixin, ExpFilterMixin
import datetime


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


class ExperimentListView(ExpFilterMixin, ListView):
    """
    View for Experiment list
    """
    model = Experiment
    template_name = 'app/experiments_page.html'

@login_required
def experiment(request, exp_id):
    company = request.user.company
    user = get_user(request)

    this_experiment = get_object_or_404(Experiment, company=company,
        id=exp_id)

    metadata = json.dumps(this_experiment.metadata)

    comments = Comment.objects.filter(experiment = this_experiment).order_by('id')
    return render(request,"app/experiment.html", {"this_experiment": this_experiment, "usr": user, "metadata": metadata, "comments": comments})


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


def analysis_page(request):
    company = request.user.company
    all_tags = Tag.objects.filter(company=company)
    all_groups = Project.objects.filter(company=company)
    return render(request, "app/analysis.html", {"usr":get_user(request), "tags":all_tags, "groups":all_groups})


class ProjectListView(CompanyObjectsMixin, ListView):
    model = Project
    template_name = 'app/project_list.html'


def create_project(request):
    """
    View for creating new projects.
    """
    if request.method == "POST":
        company = request.user.company
        project_form = ProjectForm(request.POST)

        if project_form.is_valid():
            project = project_form.save(commit=False)
            project.company = company
            project.save()

            return redirect("/app/projects")

    if request.method == "GET":
        project_form = ProjectForm()

    context = {"form": project_form}

    return render(request, 'app/create_project.html', context)


def project_page(request, p_id):
    """
    View for displaying the details of a project.
    """
    company = request.user.company

    try:
        project = Project.objects.get(company=company, id=p_id)
    except Project.DoesNotExist:
        raise Http404("Project not found")

    experiments = Experiment.objects.filter(company=company, project=p_id)

    context = {
        "experiments": experiments,
        "project": project,
        "user_count": experiments.values_list("user").distinct("user").count()
    }

    return render(request, "app/view_project.html", context)


@login_required
def create_tag(request):
    if request.method == "POST":
        tag = request.POST.get("tag")
        Tag.objects.create(name=tag, company=request.user.company)

        return HttpResponse(status=201)

    raise Http404
