from django.db import models
from accounts.models import Company
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import Group

# Create your models here.


class Settings(models.Model):
    DATE_FORMAT_CHOICES = (
        ("YYYY-MM-DD", "YYYY-MM-DD"),
        ("MM-DD-YYYY", "MM-DD-YYYY"),
        ("DD-MM-YYYY", "DD-MM-YYYY"),
        )
    company = models.ForeignKey(Company, on_delete = models.CASCADE)
    dateformat = models.CharField(max_length=11, choices=DATE_FORMAT_CHOICES, default=DATE_FORMAT_CHOICES[0][0])
    ataglance = JSONField(default = {})  # May change in the future


class GroupExtra(models.Model):
    """
    Creates a one-to-one with Django's user Group objects, allowing
    a company can add custom permission groups with a description
    """
    group = models.OneToOneField(Group, related_name="extra", on_delete=models.CASCADE)
    description = models.CharField(max_length=255, blank=True)
    company = models.ForeignKey(Company, on_delete = models.CASCADE)
