from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .forms import csvUpload
from .csvParser import read_csv
from .models import Experiment, ExperimentData
from io import TextIOWrapper
from .forms import MetadataForm
from .forms import ExperimentDataForm
import json
from .models import Template
from django.contrib.auth import get_user

# Create your views here.

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
   
    header_list = ["ID", "Chambers","Diameter","Length","Target","Age (mL)"]
    
    context = {"experiments":experiments,
               "header_list":header_list,
               "usr":user,
    }
    return HttpResponse(template.render(context,request))
    
   
def upload_csv(request):
    user = get_user(request)
    if request.method == 'POST':
        form = csvUpload(request.POST, request.FILES)
        if form.is_valid():
            data = TextIOWrapper(request.FILES['csv_file'].file, encoding=request.encoding)
            exp_id = read_csv(data)
            return HttpResponseRedirect('/app/upload/success/' + str(exp_id))
    else:
        form = csvUpload()
        
    return render(request, 'app/upload_csv.html', {'form': form, "usr":user})
            
    
def upload_form(request):
    user = get_user(request)
    REQUIRED = ['Time [min]', 'FlowRate [mL/min]', 'Current [A]', 
    'Voltage [V]', 'KI Conc [ppm]',	'StockCFU [CFU/mL]',
    'RemainingCFU [CFU/mL]']
    
    #~ template = Template.objects.filter(id = template)
    
    if request.method == 'POST':
        metadata_form = MetadataForm(request.POST, prefix='metadata')
        exp_form = ExperimentDataForm(request.POST, prefix='exp_data')
        
        if metadata_form.is_valid() and exp_form.is_valid():
            metadata = metadata_form.save(commit=False)
            # add missing fields to metadata here
            metadata.save()
            data = json.loads(exp_form.cleaned_data.get('json'))
            for row in data:
                exp_data = json.dumps(row)
                data = ExperimentData(experiment=metadata, 
                experimentData=exp_data)
        
            return HttpResponseRedirect('/app/upload/success/' + str(metadata.id))
            
        #~ return some error if form not valid

    else:
        metadata_form = MetadataForm(prefix='metadata')
        exp_form = ExperimentDataForm(prefix='exp_data')
        
        context = {'meta_form' : metadata_form, 'exp_form' : exp_form, 
        'fixed_headers' : REQUIRED, 'template' : [], 
                   'num_headers' : range(len(REQUIRED)),
        'usr':user}    

        
    return render(request, 'app/upload_form.html', context )
        
        
#~ TODO: update to return a 404 if exp_id doesn't exist
def upload_success(request, exp_id):
    return render(request, 'app/upload_success.html', {'exp_id': exp_id})

def experiment(request, exp_id):
    user = get_user(request)
    this_experiment = Experiment.objects.get(id=exp_id)
    data = this_experiment.reactor_age
    return render(request,"app/experiment.html", {"this_experiment":this_experiment, "data":data, "usr":user})
    

def userpage(request, usr_id):
    return HttpResponse(usr_id)
