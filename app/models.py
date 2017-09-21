from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField

# Create your models here.

class Experiment(models.Model):
    #~ scientist = models.ForeignKey(Scientist)
    #~ experimentMeta = JSONField()
    #person = models.CharField(max_length = 255, default = '')
    reactor_diameter = models.FloatField("Reactor Diameter [inch]", default = 0)
    reactor_length = models.FloatField("Reactor Length [inch]", default = 0)
    num_chambers = models.IntegerField("# Chambers", default = 0)
    #date = models.DateField("Date (d/m/y)", default = None)
    removal_target = models.CharField("Removal Target", max_length = 255, default = 0)
    reactor_age = models.FloatField("Age of Reactor", default = 0)
     	
class ExperimentData(models.Model):
    experiment = models.ForeignKey(Experiment)
    experimentData = JSONField()
    #More Experiment Data Here

# to make sure we have consistent field naming for searching
class Fields(models.Model):
    name = models.CharField(max_length = 255)

# to keep from having to add the same fields every time.
class Template(models.Model):
    name = models.CharField(max_length = 255)
    fields = models.ManyToManyField(Fields)
    
