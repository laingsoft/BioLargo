from channels.handler import AsgiHandler
from app.models import Tag, Group, Experiment, ExperimentData
import json


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
        "text":json.dumps(list(headset)),
    })
        

def getdata(data):
    pass

ANALYTICS_OBJECTS = {"getcols": getcols, "getdata":getdata}

def ws_analytics_columns(tagsgroups):
    data = json.loads(tagsgroups.content['text'])
    print(ANALYTICS_OBJECTS[data['action']](data['data'], tagsgroups))
    '''
    for keya in search:
        print(search[keya]['table'])
        tags.append(search[keya]['id']) if search[keya]['table'] == 'tag' else groups.append(search[keya]['id'])

    
    '''
