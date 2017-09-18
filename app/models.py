from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField

# Create your models here.

class Scientist(models.Model):
    user = models.ForeignKey(User)
    #More Scientist Data Here

class Experiment(models.Model):
    #~ scientist = models.ForeignKey(Scientist)
    #~ experimentMeta = JSONField()
    
    person = models.CharField(max_length = 255)
    reactor_diameter = models.FloatField("Reactor Diameter [inch]")
    reactor_length = models.FloatField("Reactor Length [inch]")
    num_chambers = models.IntegerField("# Chambers")
    date = models.DateField("Date (d/m/y)")
    removal_target = models.CharField("Removal Target", max_length = 255)
    reactor_age = models.FloatField("Age of Reactor")
	
	
class ExperimentData(models.Model):
    experiment = models.ForeignKey(Experiment)
    experimentData = JSONField()
    #More Experiment Data Here
