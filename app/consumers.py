from django.db.models.functions import TruncDay
from django.db.models import Count
from channels.generic.websocket import JsonWebsocketConsumer
from datetime import datetime, timedelta
import pytz


class IndexStatConsumer(JsonWebsocketConsumer):
    '''
    Provides stats for index page.
    Doesn't use channel or groups.
    '''

    # Valid actions/method names to restrict callable methods from client.
    STATS = frozenset((
        'get_daily_upload_stats',
        'get_top_uploaders',
        ))

    def connect(self):
        '''
        On connection, check if user is logged in.
        '''
        self.user = self.scope["user"]
        if self.user.is_anonymous:
            self.disconnect()

        self.accept()

    def receive_json(self, content):
        '''
        Called when text frame is recieved. Calls method
        based on 'action' parameter sent by client.
        arguments:
            - content: decoded JSON.
        '''
        action = content.get("action")
        if action not in IndexStatConsumer.STATS:
            pass  # TODO: send error if method doesn't exist or not callable.

        getattr(self, action)()  # calls method based on name.

    def get_week(self):
        '''
        Gets current week, starting on Sunday.
        '''
        today = datetime.now(pytz.utc)  # utcnow for timezone support
        start = today - timedelta(days=(today.weekday() + 1) % 7)
        end = start + timedelta(days=7)

        return (start.date(), end.date())

    def get_daily_upload_stats(self):
        '''
        Gets the number of of experiments uploaded per day for the current
        week
        '''
        week = self.get_week()
        qs = self.user.company.experiment_set.filter(
            create_timestamp__gte=week[0],
            create_timestamp__lt=week[1]) \
            .annotate(day=TruncDay('create_timestamp'))\
            .values('day') \
            .annotate(count=Count('id')) \
            .values('day', 'count')

        data = {i['day'].strftime("%a %b %d"): i['count'] for i in qs}

        current = week[0]

        while current < week[1]:
            datestring = current.strftime("%a %b %d")
            if datestring not in data:
                data[datestring] = 0
            current += timedelta(days=1)

        self.send_json({'action': 'get_daily_upload_stats', 'data': data})

    def get_top_uploaders(self):
        '''
        Gets the top 10 users with the highest number of uploads this week
        '''
        week = self.get_week()
        qs = self.user.company.experiment_set.filter(
            create_timestamp__gte=week[0],
            create_timestamp__lt=week[1]) \
            .values('user') \
            .annotate(count=Count('id')) \
            .values('user__first_name', 'count') \
            .order_by('count')[:10]

        data = {i['user__first_name']: i['count'] for i in qs}
        self.send_json({'action': 'get_top_uploaders', 'data': data})
