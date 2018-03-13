# import json
# from django.db.models.functions import TruncDay
# from django.db.models import Count
# from accounts.models import User
# from channels.auth import channel_session_user, channel_session_user_from_http
# from .models import Experiment


# def getUploadsPerUser(data, channel):
#     '''
#     Populates the section "Most Active Users"
#     '''
#     company_users = User.objects.filter(company=channel.user.company).annotate(num_exp=Count('experiment'))
#     retval = {}

#     for user in company_users:
#         retval[user.first_name] = user.num_exp

#     retval = {"data":retval, "action":"showUserUploadGraph"}
#     channel.reply_channel.send({
#         "text":json.dumps(retval)
#         })


# def getUserStats(data, channel):
#     '''
#     Fills in the "Number of Experiments Uploaded" graph. I really should rename these
#     '''
#     uploads_dates = Experiment.objects.filter(company = channel.user.company)\
#                     .annotate(day=TruncDay('create_timestamp'))\
#                     .values('day')\
#                     .annotate(count =Count('id'))\
#                     .values('day', 'count')

#     tupl = {}
#     for i in uploads_dates:
#         tupl[i['day'].strftime("%a %b %d")] = i['count']

#     retval = {"data":tupl, "action":"userstats"}
#     channel.reply_channel.send({
#         "text":json.dumps(retval)
#         })


# INDEX_OBJECTS = {"getUserStats": getUserStats, "getUploadsPerUser":getUploadsPerUser}


# @channel_session_user
# def ws_index_page(consumable):
#     '''
#     Serves as the dispacher for the websocket for the index page.
#     '''
#     data = json.loads(consumable.content['text'])
#     INDEX_OBJECTS[data['action']](data['data'], consumable)

# @channel_session_user_from_http
# def ws_index_connect(consumable):
#     '''
#     Handles the incoming connection for the websocket.
#     It's not really necessary, but we need to be able to get the user object
#     Because of how channels optimises the data sent of the wire, if we don't
#     grab the user object at connection, we never get it.
#     '''
#     consumable.reply_channel.send({'accept':True})
