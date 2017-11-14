from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from app.models import *

# Create your views here.

def index():
    pass

@login_required      
def templates(request):
    if request.method == 'GET':
        template_name = request.GET.get('template', '')
        
        try:
            fields = Template.objects.filter(name = template_name)[0].fields.all()
            fields = [field.name for field in fields]
        except IndexError:
            fields = ['']
            

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
            
    return JsonResponse({'fields' : fields})



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
            

def get_experimentbyid(request, exp_id):
    data = ExperimentData.objects.filter(experiment=exp_id)
    newval = {}
    newval = {k: v.experimentData for k,v in enumerate(data)}
    return JsonResponse(newval)

def get_experiments_id(request):
    data = Experiment.objects.all()
    data = {k: v.id for k,v in enumerate(data)}
    return JsonResponse(data)
    
def get_csv():
    pass

def experimentrm():
    pass


