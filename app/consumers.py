from channels.handler import AsgiHandler
from app.models import Tag, Group, Experiment, ExperimentData
import json
from django.db.models.functions import TruncDay
from django.db.models import Count
from accounts.models import User
from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http

def getcols(data, channel):
    tags = []
    groups = []
    for tag in data:
        print(data[tag])
        tags.append(data[tag]['id']) if data[tag]['table'] == 'tag' else groups.append(data[tag]['id'])

    
#For the love of god please clean up this absolute mess of a function.
    tagset = ExperimentData.objects.filter(experiment__tags__name__in = tags)
    headers = []
    [headers.append(v.experimentData) for k,v in enumerate(tagset)]
    
    headset = set()
    [{headset.add(header) for header in v} for k,v in enumerate(headers)] #lol nice runtime performance here 
    print(headset)
    
    channel.reply_channel.send({
        "text":json.dumps({'action':'putcols', 'data':list(headset)}),
    })
        

def getdata(data, channel):
    print(data)
    tags = []
    groups = []
    for tag in data['tags']:
        tags.append(tag['id']) if tag['table'] == 'tag' else groups.append(tag)

    xcols = []
    for xcol in data['xcols']:
        xcols.append(xcol['col'])
        
    ycols = []
    for ycol in data['ycols']:
        ycols.append(ycol['col'])

    #print(tags)
    query = ExperimentData.objects.filter(experiment__tags__name__in = tags).only("experimentData", 'experiment')
    #[print(i.id) for i in query]
    nquery = []
    retval = {}
    for i in query:
        nquery.append(i)
        retval[i.id] = {'x_ax': [], 'y_ax': [], 'exp_id':i.experiment.id}
    query = nquery

    for i in xcols:
        for y in query:
            retval[y.id]['x_ax'].append({i: y.experimentData[i]})
    for i in ycols:
        for y in query:
            retval[y.id]['y_ax'].append({i: y.experimentData[i]})
            
    retval = {'action':'putdata', 'data':retval}
    channel.reply_channel.send({
        "text":json.dumps(retval),
    })
    
        

ANALYTICS_OBJECTS = {"getcols": getcols, "getdata":getdata}

def ws_analytics_columns(tagsgroups):
    data = json.loads(tagsgroups.content['text'])
    ANALYTICS_OBJECTS[data['action']](data['data'], tagsgroups)
    '''
    for keya in search:
        print(search[keya]['table'])
        tags.append(search[keya]['id']) if search[keya]['table'] == 'tag' else groups.append(search[keya]['id'])

    
    '''




#def num_uploads(data, channel):
#    experiment_query = Experiments.objects.all().order_by("created_at")[:10]
#    dates = []
#    for experiment in experiment_query:
 #       dates.append(experiment.created_at)
  #  dateset = set(dates)
   # retval = {}
   # for i in dateset:
   #     retval[i] = dates.count(i)
   # channel.reply_channel.send({
   #     "text":json.dumps(retval),
   #     })


def getUploadsPerUser(data, channel):
    company_users = User.objects.filter(company=channel.user.company).annotate(num_exp=Count('experiment'))
    retval = {}

    for user in company_users:
        retval[user.first_name] = user.num_exp

    retval = {"data":retval, "action":"showUserUploadGraph"}
    channel.reply_channel.send({
        "text":json.dumps(retval)
        })
    

    


        

def getUserStats(data, channel):
    uploads_dates = Experiment.objects.filter(company = channel.user.company)\
                    .annotate(day=TruncDay('create_timestamp'))\
                    .values('day')\
                    .annotate(count =Count('id'))\
                    .values('day', 'count')

    tupl = {}
    for i in uploads_dates:
        tupl[i['day'].strftime("%a %b %d")] = i['count']

    retval = {"data":tupl, "action":"userstats"}
    channel.reply_channel.send({
        "text":json.dumps(retval)
        })



INDEX_OBJECTS = {"getUserStats": getUserStats, "getUploadsPerUser":getUploadsPerUser}
                                
@channel_session_user
def ws_index_page(consumable):
    '''
    Serves as the dispacher for the websocket for the index page. 
    '''
    print(consumable.user)
    data = json.loads(consumable.content['text'])
    INDEX_OBJECTS[data['action']](data['data'], consumable)

@channel_session_user_from_http
def ws_index_connect(consumable):
    '''
    Handles the incoming connection for the websocket. 
    It's not really necessary, but we need to be able to get the user object
    Because of how channels optimises the data sent of the wire, if we don't 
    grab the user object at connection, we never get it. 
    '''
    print("User Connected" + str(consumable.user))
    consumable.reply_channel.send({'accept':True})
