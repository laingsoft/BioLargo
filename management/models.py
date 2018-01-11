from django.db import models
from accounts.models import Company
from django.contrib.postgres.fields import JSONField

# Create your models here.


class Settings(models.Model):
    DATE_FORMAT_CHOICES = (
        ("YYYY-MM-DD", "YYYY-MM-DD"),
        ("MM-DD-YYYY", "MM-DD-YYYY"),
        ("DD-MM-YYYY", "DD-MM-YYYY"),
        )
    company = models.ForeignKey(Company)
    dateformat = models.CharField(max_length=11, choices=DATE_FORMAT_CHOICES, default=DATE_FORMAT_CHOICES[0][0])
    ataglance = JSONField(default = {})  # May change in the future
