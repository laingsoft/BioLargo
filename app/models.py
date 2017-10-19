from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField

# Create your models here.

class Group(models.Model):
    name = models.CharField(max_length = 255)
    
    def __str__(self):
        return self.name
        
        
class Tag(models.Model):
    name = models.CharField(max_length = 255)
    def __str__(self):
        return self.name

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
    group = models.ForeignKey(Group)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return ("Experiment| Group: {0}, Chambers: {1}, Target: {2}".format(str(self.group), str(self.num_chambers),str(self.removal_target)))

    def __repr__(self):
        return ("Experiment| Group: {0}, Chambers: {1}, Target: {2}".format(str(self.group), str(self.num_chambers),str(self.removal_target)))

     	
class ExperimentData(models.Model):
    experiment = models.ForeignKey(Experiment)
    experimentData = JSONField()
    #More Experiment Data Here


class ExperimentMetaData(models.Model):
    experiment = models.ForeignKey(Experiment)
    experimentMetaData = JSONField()


# to make sure we have consistent field naming for searching
class Fields(models.Model):
    name = models.CharField(max_length = 255)
    
    def __str__(self):
        return self.name

class Template(models.Model):
    name = models.CharField(max_length = 255)
    fields = models.ManyToManyField(Fields)
   
    def __str__(self):
        return self.name
        
class Comment(models.Model):
    user = models.ForeignKey(User)
    experiment = models.ForeignKey(Experiment)
    content = models.CharField(max_length = 255)

    
    
