from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField


class Session(models.Model):
    """
    Stores session metadata.
    """
    name = models.CharField(max_length=30)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    dataset = JSONField()  # queryset parameters.

    class Meta:
        unique_together = (('user', 'name'))

    def generate_qs(self):
        """
        uses dataset parameters (dictionary) to generate a queryset.
        """
        pass


class Action(models.Model):
    """
    stores action as JSON sent from the client and links to a session.
    action will include what the action was, the settings for the specific
    action (whatever is needed to generated object with js), what is needed to
    get data set (if using subset of data in session)
    """
    session = models.ForeignKey(Session)
    action = JSONField()
