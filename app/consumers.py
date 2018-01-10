from channels.handler import AsgiHandler
from app.models import Tag, Group, Experiment, ExperimentData
import json
from django.db.models.functions import TruncDay
from django.db.models import Count

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




def num_uploads(data, channel):
    experiment_query = Experiments.objects.all().order_by("created_at")[:10]
    dates = []
    for experiment in experiment_query:
        dates.append(experiment.created_at)
    dateset = set(dates)
    retval = {}
    for i in dateset:
        retval[i] = dates.count(i)
    channel.reply_channel.send({
        "text":json.dumps(retval),
        })
        

def getUserStats(data, channel):
    uploads_dates = Experiment.objects\
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



INDEX_OBJECTS = {"getUserStats": getUserStats}
def ws_index_page(consumable):
    print("this is a test")
    data = json.loads(consumable.content['text'])
    INDEX_OBJECTS[data['action']](data['data'], consumable)
    
