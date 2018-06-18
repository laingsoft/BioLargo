from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from project_management.models import Project

class Session(models.Model):
    """
    Stores session info and project used in analysis.
    """
    name = models.CharField(max_length=30)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    project = models.ForeignKey(Project)

    class Meta:
        unique_together = (('user', 'name'))


class Action(models.Model):
    """
    stores action as JSON sent from the client and links to a session.
    action will include what the action was, the settings for the specific
    action (whatever is needed to generated object with js), what is needed to
    get data set, etc.
    """
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    uuid = models.CharField(max_length=36)
    action = JSONField(default=dict)
