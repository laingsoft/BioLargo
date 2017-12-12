from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.template.loader import render_to_string
from .parsers import Parser, JsonParser
from .models import *
from io import TextIOWrapper
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
import json
import csv
from .forms import FileUpload, ProjectTags, ExperimentForm, ProjectForm
from io import StringIO
from .filters import filter_experiments
from .utils import to_table

# a placeholder while this setting is not implemented
METADATA_FIELDS = ["Reactor Diameter [inch]", "Reactor Length [inch]",
"#Chambers", "Date (d/m/y)","Removal Target", "Age of reactor [L]"]


@login_required
def index(request):
    """
    Index should be the main landing page for the application. It will show
    all of the available data to the researcher, and allow them to link to
    other resources, such as uploading and analysis.
    """

    company = request.user.company

    latest = Experiment.objects.filter(company=company).order_by('-id').values_list('metadata', flat=True)[:10]
    metadata_fields = METADATA_FIELDS
    latest_table = to_table(latest, metadata_fields)

    return render(request, 'app/index.html', {'latest_table': latest_table})


@login_required
def upload(request):
    """
    View for uploading data through form or upload.
    Will accept any file format supported by the parser.
    The form itself sends JSON.

    """
    company = request.user.company

    if request.method == "POST":
        project_tags = ProjectTags(request.POST, prefix='tags', company=company)
        file_form = FileUpload(request.POST, request.FILES, prefix='file_form')
        exp_form = ExperimentForm(request.POST, prefix='exp_form', company=company)

        if project_tags.is_valid() and (file_form.is_valid() or exp_form.is_valid()):
            project = project_tags.cleaned_data.get('project')
            tags = project_tags.cleaned_data.get('tags')

            if file_form.is_valid():
                pass

            elif exp_form.is_valid():
                pass

            return redirect("/app/upload/success/" + str(exp.id))


    if request.method == "GET":
        project_tags = ProjectTags(prefix = 'tags', company = company)
        file_form = FileUpload(prefix = 'file_form')
        exp_form = ExperimentForm(prefix='exp_form', company=company)

    # to handle errors, the context declaration is here.
    context = {
        'project_tags' : project_tags,
        'file_form' : file_form,
        'exp_form' : exp_form
    }

    return render(request, 'app/upload.html', context)

# # Renders form and handles file uploads
# @login_required
# def upload_file(request):
#     company = request.user.company

#     if request.method == "POST":
#         groups_tags = ProjectTags(request.POST, prefix="tags")
#         file_upload = FileUpload(request.POST, request.FILES, prefix="file")

#         if groups_tags.is_valid() and file_upload.is_valid():
#             # groups and tags are created/fetched on validation.
#             g = groups_tags.cleaned_data.get('group')
#             t = groups_tags.cleaned_data.get('tags')

#             # parse the file.
#             try:
#                 parser = Parser(fp = TextIOWrapper(request.FILES['file-upload_file'], encoding=request.encoding),
#                 metadata_fields = METADATA_FIELDS,
#                 user = request.user,
#                 file_type = "CSV"
#                 )
#             except KeyError:
#                 return HttpResponseBadRequest('File type not supported')

#             # show user the parsed data (Implement eventually)
#             parser = parser.get_parser()
#             parser.create_objects(g, t)

#             return HttpResponseRedirect('/app/upload/success/' + str(parser.get_experiment()))

#         return HttpResponse("Error uploading experiment")

#     if request.method == "GET":
#         # TODO: fill in the template here.
#         form = FileUpload(prefix="file")
#         return HttpResponse(render_to_string('app/file_upload.html', {'form': form}))

#     return HttpResponseNotFound('<h1>Page not found</h1>') # change to more appropriate error later

# # Renders form and handles form uploads
# @login_required
# def upload_form(request):
#     company = request.user.company

#     if request.method == "POST":
#         group_tags = ProjectTags(request.POST, prefix="tags")
#         experiment_data = ExperimentForm(request.POST, prefix = 'data')
#         if group_tags.is_valid() and experiment_data.is_valid():

#             # get group and tags (created on validation)
#             g = group_tags.cleaned_data.get('group')
#             t = group_tags.cleaned_data.get('tags')

#             # get string from experiment_data
#             data = experiment_data.cleaned_data.get("json")

#             # TODO:
#             # get metadata fields for user's company

#             # create parser
#             parser = JsonParser(StringIO(data), request.user, METADATA_FIELDS)

#             # create objects
#             parser.create_objects(g, t)

#             # redirect to success
#             return HttpResponseRedirect('/app/upload/success/' + str(parser.get_experiment()))


#     if request.method == "GET":
#         # get metdata template
#         # create ExperimentForm
#         experiment_data = ExperimentForm(prefix = 'data')
#         metadata = METADATA_FIELDS #TODO: get the template from database

#         # put in dictionary
#         context = {
#             'experiment_data': experiment_data,
#             'metadata': metadata,
#             'templates': Template.objects.filter(company=company).values_list('name', flat=True)
#         }
#         return HttpResponse(render_to_string('app/form_upload.html', context))

#     return HttpResponseNotFound('<h1>Page not found</h1>')

# used to get template (used for form upload)
# @login_required
# def get_template(request):
#     View used to
#     company = request.user.company

#     if request.method == 'GET':
#         template_name = request.GET.get('template', '')

#         try:
#             fields = Template.objects.filter(company= company, name = template_name)[0].fields.all()
#             fields = [field.name for field in fields]
#         except IndexError:
#             fields = ['']

#     return JsonResponse({'fields' : fields})


# Response for successful upload.
@login_required
def upload_success(request, exp_id):
    get_object_or_404(Experiment, id=exp_id)
    return render(request, 'app/upload_success.html', {'exp_id': exp_id})


@login_required
def experiment_list_view(request):
    return render(request, 'app/experiments_page.html', {})


@login_required
def experiment(request, exp_id):
    company = request.user.company
    user = get_user(request)

    this_experiment = Experiment.objects.get_object_or_404(company=company,
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


#~ From get request:
    #~ pageIndex     // current page index
    #~ pageSize      // the size of page
    #~ group
    #~ tags
    #~ sortField     // the name of sorting field
    #~ sortOrder     // the order of sorting as string "asc"|"desc"
    #~ experiment_data_filters[]
    #~ metadata_filters[]

#~ returns
#~ {
    #~ data          // array of items
    #~ itemsCount    // total items amount
#~ }
@login_required
def experiments_list(request):
    company = request.user.company
    if request.method == 'GET':

        filters = {}

        page = int(request.GET.get("pageIndex", 1))
        filters['limit'] = int(request.GET.get("pageSize", 0))
        filters['offset'] = (page - 1) * filters['limit']

        filters['order_by'] = (request.GET.get("sortField", 'id'),
        request.GET.get("sortOrder", 'asc'))

        exp_id = request.GET.get('id')
        if exp_id:
            filters['id'] = exp_id


        # filters for metadata and experiment data
        metadata_filters = request.GET.getlist("metadata_filters[]", [])
        filters['metadata_filters'] = {val.split('=')[0] : val.split('=')[1] for val in metadata_filters}

        experiment_filters = request.GET.getlist("experiment_filters[]", [])
        filters['experiment_filters'] = {val.split('=')[0]: val.split('=')[1] for val in experiment_filters}

        filters['group'] = request.GET.get('group', '')
        tags = request.GET.get('tags', '')
        if tags:
            filters['tags'] = tags.split(',')

        data, itemsCount = filter_experiments(**filters)

        # change data format to match what is used by table
        data = list(data.values('id', 'metadata'))

        for item in data:
            item.update(item['metadata'])
            del item['metadata']

        return JsonResponse({'data': data, 'itemsCount': [itemsCount]})


def project_list(request):
    """
    View to display a list of all projects within the authenticated user's
    company.
    """
    company = request.user.company
    projects = Project.objects.filter(company=company)

    return render(request, 'app/project_list.html', {'projects': projects})


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
        "project": project
    }

    return render(request, "app/view_project.html", context)
