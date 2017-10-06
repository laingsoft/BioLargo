from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.template import loader
from .csvParser import read_csv
from .models import Experiment, ExperimentData
from .models import Template, Fields
from .models import Group
from .models import Tag
from io import TextIOWrapper
from .forms import uploadForm
from .forms import csvUpload
from .forms import GroupsTags
from django.contrib.auth import get_user
import json, csv

# Create your views here.


DEFAULT_TEMPLATE = "Disinfection(bacteria)"
HEADER_LIST = ["ID", "Chambers","Diameter","Length","Target","Age (mL)"]


def index(request):
    '''
    Index should be the main landing page for the application. It will show
    all of the available data to the researcher, and allow them to link to 
    other resources, such as uploading and analysis
    '''
    user = get_user(request)
    template = loader.get_template('app/index.html')
    #experiments = [[1,2,3,4,5,6,7, 8, 9]]
    experiments = Experiment.objects.values_list()
    
    context = {"experiments":experiments,
               "header_list":HEADER_LIST,
               "usr":user,
    }
    return HttpResponse(template.render(context,request))
    
   
def upload(request):
    user = get_user(request)
    if request.method == 'POST':
        
        groups_tags = GroupsTags(request.POST, prefix="tags")

        g = None
        tags = []
        
        if groups_tags.is_valid():
            
            g = groups_tags.cleaned_data.get('group')
            g = Group.objects.get_or_create(name=g)[0]
            
            t = groups_tags.cleaned_data.get('tags')
            
            for tag in t:
                tags.append(Tag.objects.get_or_create(name=tag)[0])
            
        else:
            return HttpResponseRedirect('/app/upload/error/')
        
        csv_file = csvUpload(request.POST, request.FILES, prefix="csv")

        if csv_file.is_valid():
            data = TextIOWrapper(request.FILES['csv-csv_file'].file, encoding=request.encoding)
            exp = read_csv(data, g)
            
            exp.tags.add(*tags)
            exp.save()
    
            return HttpResponseRedirect('/app/upload/success/' + str(exp.id))
            
            
        exp_form = uploadForm(request.POST, prefix='form')
        
        if exp_form.is_valid():
            data = json.loads(exp_form.cleaned_data.get('json'))
            
            temp = []
            for row in data:
                if any(row.values()):
                    temp.append(row)
            if len(temp) == 0:
                return HttpResponse(status="400")
                
            data = temp
            
            metadata = exp_form.save(commit=False)
            metadata.group = g
            metadata.save()
            metadata.tags.add(*tags)
            metadata.save()
            
            for row in data:
                parsed = {}
                for item in row:
                    try:
                        parsed[item] = ast.literal_eval(row[item])
                    except:
                        parsed[item] = row[item]
                    
                exp_data = json.dumps(parsed)
                
                data = ExperimentData(experiment=metadata, 
                experimentData=exp_data)
                data.save()
            
            
            
        
            return HttpResponseRedirect('/app/upload/success/' + str(metadata.id))
            
        return HttpResponse('Unknown Error')

    else:

        templates = Template.objects.all()
        csv = csvUpload(prefix = 'csv')
        groups_tags = GroupsTags(prefix = 'tags')
        upload_form = uploadForm(prefix = 'form')
        templates = [t.name for t in templates]
        
        context = {'upload_form' : upload_form, 
        'templates':templates, 
        'usr':get_user(request), 
        'csv_form' : csv,
        'groups_tags' : groups_tags }
            
        return render(request, 'app/upload.html', context)
            
        
def get_template(request):
    if request.method == 'GET':
        template_name = request.GET.get('template', None)
        if not template_name:
            template_name = DEFAULT_TEMPLATE
        
        try:
            fields = Template.objects.filter(name = template_name)[0].fields.all()
            fields = [field.name for field in fields]
        except IndexError:
            fields = ['']
            
    return JsonResponse({'fields' : fields})
    
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
            
#~ TODO: update to return a 404 if exp_id doesn't exist
def upload_success(request, exp_id):
    return render(request, 'app/upload_success.html', {'exp_id': exp_id})

def experiment(request, exp_id):
    user = get_user(request)
    this_experiment = Experiment.objects.values_list().filter(id=exp_id)
    return render(request,"app/experiment.html", {"this_experiment":this_experiment, "usr":user, "header_list": HEADER_LIST})
    

def experiment_json(request, exp_id):
    data = ExperimentData.objects.filter(experiment=exp_id)
    newval = {}
    newval = {k: json.loads(v.experimentData) for k,v in enumerate(data) }
    return JsonResponse(newval)


def fields_autocomplete(request):
    if request.method == "GET":
        q = request.GET.get("q")
        result = Fields.objects.all().filter(name__icontains = q)
        
        return JsonResponse({'data' : [{'key':str(item), 'value':str(item)} for item in result]})

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
