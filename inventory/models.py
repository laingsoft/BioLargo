from django.db import models
from accounts.models import Company

# Create your models here.

class Item(models.Model):
    description = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete = models.CASCADE)

    def get_absolute_url(self):
        return "inventory/item/%i/" % self.id

class ItemField(models.Model):
    field_type = models.CharField(max_length=255)
    field_value = models.CharField(max_length=255)
    item_pointer = models.ForeignKey(Item, on_delete = models.CASCADE)
    
