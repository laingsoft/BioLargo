from django.db import models
from accounts.models import Company
from django.contrib.postgres.fields import JSONField

# Create your models here.

class Settings(models.Model):
    Company = models.ForeignKey(Company)
    dateformat = models.CharField(max_length=10)
    ataglance = JSONField() #May change in the future

