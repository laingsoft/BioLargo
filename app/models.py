from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Scientist(models.Model):
    user = models.ForeignKey(User)
    #More Scientist Data Here

class Experiment(models.Model):
    scientist = models.ForeignKey(Scientist)
    #More Experiment Data Here
