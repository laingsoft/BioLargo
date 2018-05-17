from django.db import models
from inventory.models import Item
from accounts.models import Company
from django.contrib.postgres.fields import JSONField

class SOP(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    procedure = JSONField(default = '')
    file = models.FileField(upload_to='SOP/')
    company = models.ForeignKey(Company, on_delete = models.CASCADE)

    def __str__(self):
        return self.name

class SOPMaterials(models.Model):
    SOP = models.ForeignKey(SOP, on_delete = models.CASCADE)
    amount = models.FloatField()
    item = models.ForeignKey(Item)
