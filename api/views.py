from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
import json
from app.models import *
from rest_framework import viewsets, status
from rest_framework_jwt.settings import api_settings
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .serializers import projectSerializer, commentSerializer, tagsSerializer, experimentSerializer, userSerializer, groupSerializer
from django.core.serializers import serialize
from django.http import Http404
from rest_framework.response import Response

def requestTest(request):
    print(request.body)
    return JsonResponse({"test":True})

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

def get_csv(request, exp_id):
    pass

#This will return the user's information so that it can be used to customize the client's applicaiton
@api_view(['GET'])
def get_user(request):
    user = request.user
    return Response({"email" : user.email,
                    "first_name" :user.first_name,
                    "last_name" : user.last_name})

#This generates a new Token for the user when an old token is passed in. This is used instead of
#   the default refresh_jwt_token since that was not working.
@api_view(['POST'])
def get_new_token(request):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(request.user)
    token = jwt_encode_handler(payload)
    return Response(token)


#This will delete an experiment assuming that the company is correct
#It requires an Experiment ID to be passed into it.
@login_required
def experimentrm(request, exp_id):
    company = request.user.company
    data = Experiment.objects.filter(id = exp_id, company = company)
    if not data.exists():
        raise Http404("Experiment does not exist.")
    result = data.delete()
    print("The result is", result)
    return JsonResponse({"result": result[0]>0})

@login_required
def comment(request):
    print(request.body)
    print(60*"*")
    if request.method == 'POST':
        data = json.loads(request.body)
        content = data['content']
        experiment_id = data['exp_id']
        newComment = Comment.objects.create(user = request.user, content = content, experiment = Experiment.objects.get(id=experiment_id))
        newComment.save()
        return JsonResponse({'Success':1})
    elif request.method == 'GET':
        if (request.body):
            data = json.loads(request.body)
            get_id = data['exp_id']
            comment = Comment.objects.filter(experiment = Experiment.objects.get(id = get_id))
        else:
            comment = Comment.objects.all()

        ret = {k: {'user':v.user.username, 'content':v.content, 'experiment':v.experiment.id} for k,v in enumerate(comment)}
        return JsonResponse(ret)

class resttest(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = commentSerializer

class tags(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = tagsSerializer

class experiments(viewsets.ModelViewSet):
    queryset = Experiment.objects.all()
    serializer_class = experimentSerializer

class groups(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = groupSerializer

#Retrieves the list of projects from the same company the user is part of.
class projects(APIView):
    
    def get(self, request, *args, **kwargs):
        # queryset = Project.objects.all()
        user_company = request.user.company
        serializer = projectSerializer
        project_list = Project.objects.filter(company = user_company)
        return Response(serializer(project_list, many=True).data)
    
    def post(self, request, *args, **kwargs):
        user_company = request.user.company
        
        serializer = projectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)