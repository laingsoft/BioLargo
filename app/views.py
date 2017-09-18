from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .forms.import csvUpload
from csvParser import read_csv
from .models import Experiment, ExperimentData
 
# Create your views here.

def index(request):
    template = loader.get_template('app/index.html')
    context = {}
    return HttpResponse(template.render(context,request))
    
def upload_csv(request):
    if request.method == 'POST':
        form = csvUpload(request.POST, request.FILES)
        if form.is_valid():
            exp_id = read_csv(request.FILES['csv_file'])
            return HTTPResponseRedirect('/success/' + str(exp_id))
        else:
            form = csvUpload()
        
        return render(request, 'upload_csv.html', {'form': form})
            
def upload_success(request):
    template = loader.get_template('app/upload_success.html')

    return HttpResponse(template.render({'exp_id':exp_id}, request))

