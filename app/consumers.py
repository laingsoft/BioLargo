from channels.handler import AsgiHandler
from app.models import Tag, Group, Experiment, ExperimentData
import json


def ws_analytics_columns(tagsgroups):
    search = json.loads(tagsgroups.content['text'])
    tags = []
    groups = []
    for keya in search:
        print(search[keya]['table'])
        tags.append(search[keya]['id']) if search[keya]['table'] == 'tag' else groups.append(search[keya]['id'])

    #For the love of god please clean up this absolute mess of a function.
    tagset = ExperimentData.objects.filter(experiment__tags__name__in = tags)
    headers = []
    [headers.append(json.loads(v.experimentData)) for k,v in enumerate(tagset)]
    
    headset = set()
    [{headset.add(header) for header in v} for k,v in enumerate(headers)] #lol nice runtime performance here 
    print(headset)
    
    tagsgroups.reply_channel.send({
        "text":json.dumps(list(headset)),
    })
    
