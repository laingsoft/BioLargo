from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseNotFound
from django.http import JsonResponse
from django.template.loader import render_to_string
from .parsers import Parser, JsonParser
from .models import *
from io import TextIOWrapper
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
import json
import csv
from .forms import FileUpload, GroupsTags, ExperimentForm
from io import StringIO
from .filters import filter_experiments

HEADER_LIST = ["ID", "Chambers","Diameter","Length","Target","Age (mL)"]
metadata_fields = ["Reactor Diameter [inch]", "Reactor Length [inch]", "#Chambers",	"Date (d/m/y)",	"Removal Target", "Age of reactor [L]"]

@login_required
def index(request):
    '''
    Index should be the main landing page for the application. It will show
    all of the available data to the researcher, and allow them to link to 
    other resources, such as uploading and analysis. 
    '''
    return render(request,'app/index.html', {})
    
# --------------------Views used for uploading data---------------------
# displays the upload page. Additional parts of the form and processing
# is done in other views.
@login_required
def upload(request):
    context = {
    'groups_tags' : GroupsTags(prefix = 'tags') }
        
    return render(request, 'app/upload.html', context)


# Renders form and handles file uploads
@login_required
def upload_file(request):
    if request.method == "POST":
        groups_tags = GroupsTags(request.POST, prefix="tags")
        file_upload = FileUpload(request.POST, request.FILES, prefix="file")
        
        if groups_tags.is_valid() and file_upload.is_valid():
            # groups and tags are created/fetched on validation.
            g = groups_tags.cleaned_data.get('group')
            t = groups_tags.cleaned_data.get('tags')
            
            # parse the file.
            try:
                parser = Parser(fp = TextIOWrapper(request.FILES['file-upload_file'], encoding=request.encoding), 
                metadata_fields = metadata_fields, 
                user = request.user,
                file_type = "CSV"
                )
            except KeyError:
                return HttpResponseBadRequest('File type not supported')
                
            # show user the parsed data (Implement eventually)
            parser = parser.get_parser()
            parser.create_objects(g, t)

            return HttpResponseRedirect('/app/upload/success/' + str(parser.get_experiment()))
            
        return HttpResponse("Error uploading experiment")
    
    if request.method == "GET":
        # TODO: fill in the template here.
        form = FileUpload(prefix="file")
        return HttpResponse(render_to_string('app/file_upload.html', {'form': form}))
        
    return HttpResponseNotFound('<h1>Page not found</h1>') # change to more appropriate error later

# Renders form and handles form uploads
@login_required
def upload_form(request):
    if request.method == "POST":
        group_tags = GroupsTags(request.POST, prefix="tags")
        experiment_data = ExperimentForm(request.POST, prefix = 'data')
        if group_tags.is_valid() and experiment_data.is_valid():
            
            # get group and tags (created on validation)
            g = group_tags.cleaned_data.get('group')
            t = group_tags.cleaned_data.get('tags')
            
            # get string from experiment_data
            data = experiment_data.cleaned_data.get("json")
            
            # TODO:
            # get metadata fields for user's company
            
            # create parser
            parser = JsonParser(StringIO(data), request.user, metadata_fields)
            
            # create objects
            parser.create_objects(g, t)
            
            # redirect to success
            return HttpResponseRedirect('/app/upload/success/' + str(parser.get_experiment()))

        
    if request.method == "GET":
        # get metdata template
        # create ExperimentForm
        experiment_data = ExperimentForm(prefix = 'data')
        metadata = metadata_fields #TODO: get the template from database
        
        # put in dictionary
        context = {
            'experiment_data': experiment_data,
            'metadata': metadata,
            'templates': Template.objects.all().values_list('name', flat=True)
        }
        return HttpResponse(render_to_string('app/form_upload.html', context))

    return HttpResponseNotFound('<h1>Page not found</h1>')

# used to get template (used for form upload)
@login_required      
def get_template(request):
    if request.method == 'GET':
        template_name = request.GET.get('template', '')
        
        try:
            fields = Template.objects.filter(name = template_name)[0].fields.all()
            fields = [field.name for field in fields]
        except IndexError:
            fields = ['']
            
    return JsonResponse({'fields' : fields})
    
# used to save templates on upload form. TODO: RESTRICT TO ADMIN USERS 
@login_required
def save_template(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data['name']
        fields = data['fields']
       
        if name and fields:
            # check if name already exists
            if Template.objects.filter(name=name).exists():
                return JsonResponse({'success': False, 'error': "Name already exists"})
                
            template = Template(name = name)
            template.save()
                
            f = []
            for field in fields:
                f.append(Fields.objects.get_or_create(name=field)[0])
            
            template.fields.add(*f)
            
            return JsonResponse({'success' : True})
            
        return JsonResponse({'success' : False, 'error': "Error saving template"})
        
# autocomplete results for fields        
@login_required
def fields_autocomplete(request):
    if request.method == "GET":
        q = request.GET.get("q")
        result = Fields.objects.all().filter(name__icontains = q)
        return JsonResponse({'data' : [{'key':str(item), 'value':str(item)} for item in result]})
        
# autocomplete results for groups
@login_required
def groups_list(request):
    if request.method == "GET":
        result = [str(i) for i in Group.objects.all()]
        return JsonResponse({'data' : [{'key':str(item), 'value':str(item)} for item in result]})    
            
# Response for successful upload.
@login_required
def upload_success(request, exp_id):
    get_object_or_404(Experiment, id=exp_id)
    return render(request, 'app/upload_success.html', {'exp_id': exp_id})

#------------------------Experiment Page Views--------------------------
@login_required
def experiment(request, exp_id):
    user = get_user(request)
    this_experiment = Experiment.objects.values_list().filter(id=exp_id)
    return render(request,"app/experiment.html", {"this_experiment":this_experiment, "usr":user, "header_list": HEADER_LIST})
    
@login_required
def experiment_json(request, exp_id):
    data = ExperimentData.objects.filter(experiment=exp_id)
    newval = {}
    newval = {k: v.experimentData for k,v in enumerate(data)}
    return JsonResponse(newval)


@login_required
def experimentrm(request, exp_id):
    data = Experiment.objects.filter(id=exp_id)
    res = data.delete()
    return JsonResponse({"result": res[0]>0})
    

@login_required
def experimentrm(request, exp_id):
    data = Experiment.objects.get(id=exp_id)
    res = data.delete()
    return JsonResponse({"result": res[0]>0})
    
@login_required
def get_csv(request, exp_id, header=0):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="'+exp_id+'.csv"'
    vals = ExperimentData.objects.filter(experiment=exp_id)
    newdata = []
    [newdata.append(json.loads(i.experimentData)) for i in vals]
    fieldnames = []
    [fieldnames.append(k) for k in newdata[0]]
    writer = csv.DictWriter(response, fieldnames)
    writer.writeheader()
    [writer.writerow(i) for i in newdata]
    return response

def analysis_page(request):
    all_tags = Tag.objects.all()
    all_groups = Group.objects.all()
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
        filters['experiment_filters'] = {val.split('=')[0] : val.split('=')[1] for val in experiment_filters}
        
        
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

        return JsonResponse({'data':data, 'itemsCount': [itemsCount]}) 
        
# TODO: implement this function.
def get_metadata_template(request):
    # get template from somewhere....
    metadata = list(metadata_fields)
    metadata.insert(0, 'id')
    
    return JsonResponse({'data': metadata})
