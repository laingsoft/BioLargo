from django.db import models
from inventory.models import Item
from accounts.models import Company

class SOP(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    file = models.FileField(upload_to='SOP/')
    company = models.ForeignKey(Company)


class SOPMaterials(models.Model):
    UNITS = (
        ('L', 'L'),
        ('g', 'g'),
        ('mL', 'mL'),
        )

    SOP = models.ForeignKey(Item)
    amount = models.FloatField()
    unit = models.CharField(max_length=3, choices=UNITS)
