from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.http import JsonResponse
from django.template.loader import render_to_string
from .parsers import Parser
from .models import *
from io import TextIOWrapper
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
import json
import csv
from .forms import FileUpload, GroupsTags, ExperimentForm

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
        return HttpResponse(render_to_string('app/file_upload.html', {'form': FileUpload(prefix="file")}))
        
    return HttpResponseNotFound('<h1>Page not found</h1>') # change to more appropriate error later

# Renders form and handles form uploads
@login_required
def upload_form(request):
    if request.method == "POST":
        group_tags = GroupsTags(request.POST, prefix="tags")
        experiment_data = ExperimentForm(request.POST, prefix = 'data')
        
        if group_tags.is_valid() and experiment_data.is_valid():
            pass
            
            # get group and tags (created on validation)
            # get metadata template
            # try:
            #    parse experiment data with JSON parser
            # except TypeError:
            #   return error
            # parser.create_objects(group, tags)
            
            # return success 
            
        
    if request.method == "GET":
        # get metdata template
        # create ExperimentForm
        
      
        experiment_data = ExperimentForm(prefix = 'data')
        metadata = metadata_fields #TODO: get the template from database
        
        # put in dictionary
        context = {
            'experiment_data': experiment_data,
            'metadata': metadata,
            'templates': Template.objects.all().values_list('name')
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
                
            f = []
            for field in fields:
                f.append(Fields.objects.get_or_create(name__iexact=field)[0])
            
            template.save()
            
            for field in f:
                field.save()
                template.fields.add(field)
                
            template.save()
            
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
    #~ sortField     // the name of sorting field
    #~ sortOrder     // the order of sorting as string "asc"|"desc"
    
    #~ "id" : search
    #~ "num_chambers" : search
    #~ "reactor_diameter" : search
    #~ "reactor_length" : search
    #~ "removal_target" : search
    #~ "reactor_age" : search
    #~ "group__name" : search
    #~ "tags[]" : search (list)
    #~ "fields" : search (list)

#~ returns

#~ {
    #~ data          // array of items
    #~ itemsCount    // total items amount
#~ }
@login_required
def experiments_list(request):
    if request.method == 'GET':
        
        page = int(request.GET.get("pageIndex", 1))
        size = int(request.GET.get("pageSize", 0))
        offset = (page - 1) * size
        
        sort_field = request.GET.get("sortField", 'id')
        sort_order = request.GET.get("sortOrder", 'asc')
        
        if sort_order == 'desc':
            sort_field = '-' + sort_field
            
            
        query_dict = dict(request.GET)
                    
        qs = Experiment.objects.all().values(
        'id',
        'reactor_diameter',
        'reactor_length',
        'num_chambers',
        'removal_target',
        'reactor_age',
        'group__name').order_by(sort_field)
        
        try:
            data = qs.order_by(sort_field)
        except django.core.exceptions.FieldError:
            pass
            
            
        # parse the fields search if it exists.
        try:
            query_dict['fields[]']
        except KeyError:
            # do nothing if no field keywords.
            pass
            
        #~ dictionary of all filters. 
        filters = {
            "id" : (lambda qs, q : qs.filter(id = q[0])),
            "num_chambers" : (lambda qs, q :  qs.filter(num_chambers = q[0])),
            "reactor_diameter" : (lambda qs, q :  qs.filter(reactor_diameter = q[0])),
            "reactor_length" : (lambda qs, q :  qs.filter(reactor_length = q[0])),
            "removal_target" : (lambda qs, q :  qs.filter(removal_target__icontains = q[0])),
            "reactor_age" : (lambda qs, q :  qs.filter(reactor_age = q[0])),
            "group__name" : (lambda qs, q :  qs.filter(group__name__icontains = q[0])),
            "tags[]" : (lambda qs, q :  qs.filter(tags__name__in = q).distinct()),
            "fields[]": (lambda qs , q : qs.filter(experimentdata__experimentData__contains = q).distinct())
        }
        
        for item in query_dict:
            try:
                qs = filters[item](qs, query_dict[item])
            except KeyError:
                # ignore any filters that are not in the filters dict
                pass
                
        itemsCount = qs.count()
        tags = qs.values('id', 'tags')
        data = qs[offset: offset + size]
        data = list(qs)
        
        for item in data:
            item['tags'] = ', '.join([str(i) for i in tags.filter(id=item['id']).values_list('tags__name', flat=True)])

        return JsonResponse({'data':data, 'itemsCount': [itemsCount]}) 
