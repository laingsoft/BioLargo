from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.

def index(request):
    '''
    Index should be the main landing page for the application. It will show
    all of the available data to the researcher, and allow them to link to 
    other resources, such as uploading and analysis
    '''
    template = loader.get_template('app/index.html')
    list = [1,2,3,4,5,6]
    context = {"list":list, "header_list":["Researcher", "Diameter", "Flow Rate", "KI"], "experiment_data":[["Chuck",'1"', "8mL/min","5 ppm"],["Ted",'6"',"16mL/Min","30 ppm"]]}
    return HttpResponse(template.render(context,request))
