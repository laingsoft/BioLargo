from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
import json
import datetime
from io import TextIOWrapper
from app.models import *
from accounts.models import User
from app.parsers import Parser
from rest_framework.parsers import FileUploadParser
from rest_framework import viewsets, status
from rest_framework_jwt.settings import api_settings
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .serializers import experimentDataSerializer, projectSerializer, commentSerializer, tagsSerializer, experimentSerializer, userSerializer, groupSerializer, simpleExperimentSerializer
from django.core.serializers import serialize
from django.http import Http404
from rest_framework.response import Response
from django.db import IntegrityError

def requestTest(request):
    print(request.body)
    return JsonResponse({"test":True})

def index(request):
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

#This will return the user's information so that it can be used to customize the client's applicaiton
@api_view(['GET'])
def get_user(request):
    user = request.user
    serializer = userSerializer
    return Response(serializer(user).data)

#This generates a new Token for the user when an old token is passed in. This is used instead of
#   the default refresh_jwt_token since that was not working.
@api_view(['GET'])
def get_new_token(request):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(request.user)
    token = jwt_encode_handler(payload)
    return Response(token)

@login_required
def comment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        content = data['content']
        experiment_id = data['exp_id']
        try:
            Comment.objects.create(
                user=request.user,
                content=content,
                experiment=Experiment.objects.get(id=experiment_id),
                company=request.user.company,
            )

        except IntegrityError:
            return JsonResponse({'Success':0})

        return JsonResponse({'Success':1})

    elif request.method == 'GET':
        if (request.body):
            data = json.loads(request.body)
            get_id = data['exp_id']
            comment = Comment.objects.filter(experiment = Experiment.objects.get(id = get_id))
        else:
            comment = Comment.objects.all()

        ret = {k: {'user':v.user.email, 'content':v.content, 'experiment':v.experiment.id} for k,v in enumerate(comment)}
        return JsonResponse(ret)

class resttest(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = commentSerializer

#This will get all the epxeriments that are part of the project whose ID is passed in
@api_view(['GET'])
def getExperimentsWithProjectId(request, id):
    experiments = Experiment.objects.filter(project = id)
    serializer = experimentSerializer
    return Response(serializer(experiments, many = True).data)

#This gets the comments from the experiment whose ID is passed in. 
@api_view(['GET'])
def get_exp_comments(request, id):
    comments = Comment.objects.filter(experiment = id)
    return Response(commentSerializer(comments, many = True).data)

#Get the Data from the Experiment Data model according to the experiment id passed in
@api_view(['GET'])
def getExperimentData(request, id):
    serializer = experimentDataSerializer
    experiment_data = ExperimentData.objects.filter(experiment = id)
    return Response(serializer(experiment_data, many=True).data)

@api_view(['GET'])
def getOverviewCount(request):
    user_company = request.user.company
    experiment_count = Experiment.objects.filter(company = user_company).count()
    user_count = User.objects.filter(company = user_company).count() 
    project_count = Project.objects.filter(company = user_company).count()

    #############
    currentDate = datetime.date.today()
    delta = datetime.timedelta(days=1)

    minusOne = currentDate - delta
    dayOne = Experiment.objects.filter(create_timestamp__range=[minusOne, currentDate]).count()
    minusTwo = minusOne - delta
    dayTwo = Experiment.objects.filter(create_timestamp__range=[minusTwo, minusOne]).count()
    minusThree = minusTwo - delta
    dayThree = Experiment.objects.filter(create_timestamp__range=[minusThree, minusTwo]).count()
    return JsonResponse({"experiments" : experiment_count, 
                        "projects" : project_count,
                        "users" : user_count, 
                        "first" : dayOne,
                        "second" : dayTwo, 
                        "third" : dayThree})



class tags(APIView):
    def get(self, request):
        company = request.user.company
        queryset = Tag.objects.filter(company = company)
        serializer = tagsSerializer
        return Response(serializer(queryset, many=True).data)
    def post(self, request, *args, **kwargs):
        user_company = request.user.company
        serializer = tagsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class projects(APIView):
    #Retrieves the list of projects from the same company the user is part of.
    def get(self, request, id = None):
        user_company = request.user.company
        serializer = projectSerializer
        if(id == None):
            project_list = Project.objects.filter(company = user_company)
        else:
            project_list = Project.objects.filter(id = id)
        return Response(serializer(project_list, many=True).data)
    #Post a new Project
    def post(self, request, *args, **kwargs):
        user_company = request.user.company
        serializer = projectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        company = request.user.company
        data = Project.objects.filter(id = id, company = company)
        if not data.exists():
            raise Http404("Project not found")
        result = data.delete()
        return JsonResponse({"result": result[0]>0})

        
class experiments(APIView):
    #Retrieves the list of experiments from the same company the user is part of.
    def get(self, request, id = None):
        user_company = request.user.company
        serializer = experimentSerializer
        if(id == None):
            experiment_list = Experiment.objects.filter(company = user_company)
        else:
            experiment_list = Experiment.objects.filter(id = id)
        return Response(serializer(experiment_list, many=True).data)
    #Post a new Experiment - This method uses the simplifiedExperimentSerializer which requires less data to create a new experiment.
    def post(self, request, *args, **kwargs):
        #Serialize the data from the experiment
        serializer = simpleExperimentSerializer(data=request.data)
        #Put the request's user and company information into the serializer
        serializer.user = request.user
        serializer.company = request.user.company
        #Get the file object that was passed in and parse it with the file parser
        file_obj = request.FILES['file']
        parser = Parser(buffer=TextIOWrapper(file_obj), encoding=request.encoding)
        #If the serializer is valid, save it into an experiment Object and send that object into the parser to create the finished experiment.
        if serializer.is_valid():
            experiment = serializer.save()
            parser.get_parser().create_objects(experiment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        company = request.user.company
        data = Experiment.objects.filter(id = id, company = company)
        if not data.exists():
            raise Http404("Experiment not found")
        result = data.delete()
        return JsonResponse({"result": result[0]>0})







