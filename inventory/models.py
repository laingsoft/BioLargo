from django.db import models
from accounts.models import Company

# Create your models here.

class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete = models.CASCADE)
    on_hand = models.IntegerField()
    

    def get_absolute_url(self):
        return "/inventory/item/%i" %self.id


class ItemField(models.Model):
    field_type = models.CharField(max_length=255)
    field_value = models.CharField(max_length=255)
    item_pointer = models.ForeignKey(Item, on_delete = models.CASCADE)

    def __str__(self):
        return "{1} {0}".format(str(self.field_type),str(self.field_value))


class Equipment(models.Model):
    manufacturer = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    name = models.CharField(max_length=255)


class Calibration(models.Model):
    datetime = models.DateTimeField()
    value = models.FloatField()
    equipment = models.ForeignKey(Equipment, on_delete = models.CASCADE)
