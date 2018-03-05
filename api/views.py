from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
import json
import datetime
from io import TextIOWrapper, StringIO
from app.models import *
from accounts.models import User
from app.parsers import Parser, JsonParser
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import FileUploadParser
from rest_framework import viewsets, status
from rest_framework_jwt.settings import api_settings
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from app.forms import ExperimentDataForm
from .serializers import *
from django.http import Http404
from rest_framework.response import Response
from django.db import IntegrityError
from project_management.models import Project

def index(request):
    pass

@api_view(['GET'])
def analysis_page(request):
    company = request.user.company
    all_tags = Tag.objects.filter(company=company)
    all_groups = Project.objects.filter(company=company)
    return render(request, "test.html", {"usr":request.user, "tags":all_tags, "groups":all_groups})


#This will return the user's information so that it can be used to customize the client's applicaiton
@api_view(['GET', 'POST'])
def get_user(request):
    user = request.user
    if(request.method == 'GET'):
        serializer = userSerializer
        return Response(serializer(user).data)
    else:
        request.user.first_name = request.data['first_name']
        request.user.last_name = request.data['last_name']
        request.user.email = request.data['email']
        request.user.save()
        return JsonResponse({"success":True})


@api_view(['GET'])
def get_company_users(request):
    company = request.user.company
    serializer = userSerializer
    users = User.objects.filter(company = company)
    return Response(serializer(users, many=True).data)


#This generates a new Token for the user when an old token is passed in. This is used instead of
#   the default refresh_jwt_token since that was not working.
@api_view(['GET'])
def get_new_token(request):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(request.user)
    token = jwt_encode_handler(payload)
    return Response(token)

#This will get all the epxeriments that are part of the project whose ID is passed in
@api_view(['GET'])
def get_experiments_with_project_id(request, id, page):
    experiments = Experiment.objects.filter(project = id).order_by('-id')
    serializer = experimentSerializer
    paginator = Paginator(experiments, 10)
    try:
        #Try to get the page from the paginator that was passed in.
        experiments = paginator.page(page)
    except EmptyPage:
        #Gets the last page
        experiments = paginator.page(paginator.num_pages)
    return Response(serializer(experiments, many = True).data)

#This will get the epxeriment that has the ID that is passed in
@api_view(['GET'])
def get_experiments_with_experiment_id(request, id):
    experiments = Experiment.objects.filter(id = id)
    serializer = experimentSerializer
    return Response(serializer(experiments).data)


#Get the Data from the Experiment Data model according to the experiment id passed in
@api_view(['GET'])
def get_experiment_data(request, id):
    serializer = experimentDataSerializer
    experiment_data = ExperimentData.objects.filter(experiment = id)
    return Response(serializer(experiment_data, many=True).data)


#Call this with a notification id in the URL to mark it as read
@api_view(['GET'])
def read_notification(request, id):
    n = Notification.unread.get(id=id, recipient=request.user)
    n.read = True
    n.save()    
    return JsonResponse({'success': True})

#Pass in a Task ID and it will be marked as complete 
@api_view(['GET'])
def mark_task_complete(request, id):
    task = Task.objects.get(id=id)
    task.status = "C"
    task.save()
    return JsonResponse({'success' : True})

#Pass in a Task ID and it will be marked as "in progress" 
@api_view(['GET'])
def mark_task_in_progress(request, id):
    task = Task.objects.get(id=id)
    task.status = "I"
    task.save()
    return JsonResponse({'success' : True})


@api_view(['GET'])
def get_project_stats(request, id):
    experiments = Experiment.objects.filter(project = id)
    #Get the number of experiments that the project has associated
    experiment_count = experiments.count()
    #Get the number of people that have uploaded experiments for this project id   
    tempList = []
    for each in experiments:
        if(each.user.id not in tempList):
            tempList.append(each.user.id)
    scientists = len(tempList)
    #Get the progress from the ratio of tasks todo / tasks complete
    tasks = Task.objects.filter(project = id)
    todo_count = 0
    for each in tasks:
        if(each.status == "N"):
            todo_count += 1
    if tasks.count() != 0:
        progress = 100 * (1 - (todo_count / tasks.count()))
    elif todo_count == 0:
        progress = 100
    else:
        progress = 0


    return JsonResponse({"experiment_count" : experiment_count, 
                        "progress" : "{0:.2f}".format(progress), 
                        "scientists" : scientists})


@api_view(['GET'])
def get_overview_count(request):
    #Get the counts for the amount of experiments, projects, and users for the particular company
    user_company = request.user.company
    experiment_count = Experiment.objects.filter(company = user_company).count()
    project_count = Project.objects.filter(company = user_company).count()
    user_count = User.objects.filter(company = user_company).count()

    #############
    #Get the number of experiments that was created in the user's company for the past three days.
    currentDate = datetime.date.today()
    delta = datetime.timedelta(days=1)

    minusOne = currentDate - delta
    dayOne = Experiment.objects.filter(create_timestamp__range=[minusOne, currentDate]).count()
    minusTwo = minusOne - delta
    dayTwo = Experiment.objects.filter(create_timestamp__range=[minusTwo, minusOne]).count()
    minusThree = minusTwo - delta
    dayThree = Experiment.objects.filter(create_timestamp__range=[minusThree, minusTwo]).count()

    #############
    #Get all the unread notifications that the user should see.
    notifications = notificationSerializer(Notification.objects.filter(read=False,
        recipient = request.user), many = True).data

    return JsonResponse({"experiments" : experiment_count,
                        "projects" : project_count,
                        "users" : user_count,
                        "first" : dayOne,
                        "second" : dayTwo,
                        "third" : dayThree,
                        "notifications": notifications})

#Will return the tasks that are associated with the status that is passed in: N, I, C
# and will allow for pagination of the tasks      
@api_view(['GET'])
def get_tasks(request, status, page):
    #Get the project ids for any projects that have tasks assigned to this user
    tasks = Task.objects.filter(status = status, company=request.user.company, assigned = request.user).order_by('-id')
    paginator = Paginator(tasks, 10)
    try:
        #Try to get the page from the paginator that was passed in.
        tasks = paginator.page(page)
    except EmptyPage:
        #Gets the last page
        tasks = paginator.page(paginator.num_pages)
    return Response(TaskSerializer(tasks, many=True).data)


#Will toggle a "Watch" on both experiments and/or projects
#Requires an experiment/project id and a type as to differentiate between EXP or PRJ
@api_view(['POST'])
def watch(request):
    ObjectTypes = {'EXP': Experiment, 'PRJ': Project}
    object_id = request.POST['id']
    object_type = request.POST['type']
    if ObjectTypes[object_type].objects.filter(id=object_id).exists():
        obj = ObjectTypes[object_type].objects.get(id=object_id)
        #If the user is already following this particular object, then remove them from the list
        if obj.followers.filter(id=request.user.id).exists():
            obj.followers.remove(request.user)
            return JsonResponse({'watched': False})
        #Add the user to the list of followers
        else:
            obj.followers.add(request.user)
            return JsonResponse({'watched': True})
    return JsonResponse({'success': False})


class tags(APIView):
    def get(self, request):
        company = request.user.company
        queryset = Tag.objects.filter(company = company)
        serializer = tagsSerializer
        return Response(serializer(queryset, many=True).data)

    def post(self, request, *args, **kwargs):
        serializer = tagsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class projects(APIView):
    #Retrieves the list of projects from the same company the user is part of.
    def get(self, request, page):
        user_company = request.user.company
        serializer = projectSerializer
        # Get the list of projects form the user's company
        project_list = Project.objects.filter(company = user_company).order_by('-id')
        #Setup the paginator on the project list, 10 per page
        paginator = Paginator(project_list, 10)
        try:
            #Try to get the page from the paginator that was passed in.
            project_list = paginator.page(page)
        except EmptyPage:
            #Gets the last page
            project_list = paginator.page(paginator.num_pages)
        return Response(serializer(project_list, many=True).data)
    #Post a new Project
    def post(self, request, *args, **kwargs):
        if(request.user.is_manager):
            user_company = request.user.company
            serializer = projectSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        if(request.user.is_manager):
            company = request.user.company
            data = Project.objects.filter(id = id, company = company)
            if not data.exists():
                raise Http404("Project not found")
            result = data.delete()
            return JsonResponse({"result": result[0]>0})
        return Response(status=status.HTTP_400_BAD_REQUEST)


class experiments(APIView):
    #Retrieves the list of experiments from the same company the user is part of.
    def get(self, request, page):
        user_company = request.user.company
        serializer = experimentSerializer
        experiment_list = Experiment.objects.filter(company = user_company).order_by('-id')
        paginator = Paginator(experiment_list, 10)
        try:
            #Try to get the experiemnts on the page number that is passed in
            experiment_list = paginator.page(page)
        except EmptyPage:
            #If the page we treid to get is empty, return the last page instead
            project_list = paginator.page(paginator.num_pages)
        return Response(serializer(experiment_list, many=True).data)
    #Post a new Experiment - This method uses the simplifiedExperimentSerializer which requires less data to create a new experiment.
    def post(self, request, *args, **kwargs):
        #Serialize the data from the experiment
        serializer = simpleExperimentSerializer(data=request.data)
        #Put the request's user and company information into the serializer
        serializer.user = request.user
        serializer.company = request.user.company
        #Get the file object that was passed in and parse it with the file parser
        #If there is a valid file, this will do a file upload
        try:
            file_obj = request.FILES['file']
            parser = Parser(buffer=TextIOWrapper(file_obj), encoding=request.encoding)
            #If the serializer is valid, save it into an experiment Object and send that object into the parser to create the finished experiment.
            if serializer.is_valid():
                experiment = serializer.save()
                parser.get_parser().create_objects(experiment)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #If no files were passed in, there will be a form upload. This takes care of that in the except block.
        except:
            if serializer.is_valid():
                #Get the json data from the POST request and use that to populate the Experiment Data
                json_data = json.loads(request.POST["experimentData"])
                #Make the initial experiment with no data
                experiment = serializer.save()
                #iterate through each key of the Data and make a new ExperimentData for it.
                for i in json.loads(request.POST['experimentData']):
                    ExperimentData.objects.create(experiment=experiment, experimentData=json.loads(request.POST['experimentData'])[i], company=request.user.company)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, id):
        company = request.user.company
        if(request.user.is_manager):
            data = Experiment.objects.filter(id = id, company = company)
        else:
            data = Experiment.objects.filter(user = request.user, id = id, company = company)
        if not data.exists():
            raise Http404("Experiment not found")
        result = data.delete()
        return JsonResponse({"result": result[0]>0})


class template(APIView):
    def get(self, request, id = None):
        user_company = request.user.company
        serializer = templateSerializer
        if(id == None):
            template_list = Template.objects.filter(company = user_company)
        else:
            template_list = Template.objects.filter(id = id)
        return Response(serializer(template_list, many=True).data)

    #TODO - unknown response, have not used/tested
    def post(self, request, *args, **kwargs):
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

#To post a new comment, the request body requires an experiment id (exp_id)
# and content
class comment(APIView):
    def post(self, request):
        try:
            new_comment = Comment.objects.create(
                user=request.user,
                content=request.POST['content'],
                experiment=Experiment.objects.get(id=request.POST['exp_id']),
                company=request.user.company,
            )
        except IntegrityError:
            return JsonResponse({'Success':0})
        return JsonResponse(commentSerializer(new_comment).data)
    #The get requires an id passed in through the URL to get comments
    # for that particular experiment
    def get(self, request, id):
        comments = Comment.objects.filter(experiment = id)
        return Response(commentSerializer(comments, many = True).data)