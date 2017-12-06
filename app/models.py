from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from accounts.models import Company

# Create your models here.

class Group(models.Model):
    name = models.CharField(max_length = 255)
    
    def __str__(self):
        return self.name

class Project(models.Model):
    company = models.ForeignKey(Company)
    name = models.CharField(max_length = 255)
    start = models.DateField()
    metadata_template = models.TextField()
    end = models.DateField(null = True, blank = True)
    description = models.TextField(blank = True, null = True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    company = models.ForeignKey(Company)
    name = models.CharField(max_length = 255)
    def __str__(self):
        return self.name

class Experiment(models.Model):
    # scientist = models.ForeignKey(Scientist)
    company = models.ForeignKey(Company)
    user = settings.AUTH_USER_MODEL
    project = models.ForeignKey(Project)

    group = models.ForeignKey(Group)
    tags = models.ManyToManyField(Tag)
    metadata = JSONField(default = '') 
    friendly_name = models.CharField(max_length=255, default = 0)

    def __str__(self):
        return ("Experiment| Group: {0} | metadata: {1}").format(str(self.group), str(self.metadata))

    def __repr__(self):
        return ("Experiment| Group: {0} | metadata: {1}").format(str(self.group), str(self.metadata))
     	
class ExperimentData(models.Model):
    company = models.ForeignKey(Company)
    class Meta:
        verbose_name_plural = "experiment data"
        
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    experimentData = JSONField()
    #More Experiment Data Here

# to make sure we have consistent field naming for searching
class Fields(models.Model):
    company = models.ForeignKey(Company)
    class Meta:
        verbose_name_plural: "fields"
            
    name = models.CharField(max_length = 255)
    
    def __str__(self):
        return self.name

class Template(models.Model):
    company = models.ForeignKey(Company)
    name = models.CharField(max_length = 255)
    fields = models.ManyToManyField(Fields) 
   
    def __str__(self):
        return self.name
        
class Comment(models.Model):
    company = models.ForeignKey(Company)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    content = models.CharField(max_length = 255)

    
class Activity(models.Model):
    company = models.ForeignKey(Company)
    action = models.CharField(max_length = 100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
