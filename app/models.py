from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField

# Create your models here.

class Scientist(models.Model):
    user = models.ForeignKey(User)
    #More Scientist Data Here

class Experiment(models.Model):
    scientist = models.ForeignKey(Scientist)
    experimentMeta = JSONField()
    experimentData = JSONField()
    #More Experiment Data Here
