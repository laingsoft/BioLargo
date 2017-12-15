from django.db import models

from inventory.models import Item

class OpSteps(models.Model):
    text = models.CharField(max_length = 1000)
    step_number = models.IntegerField()
    op = models.ForeignKey(OperatingProcedure)
    

class OpMaterials(models.Model):
    '''
    Provides a connection between the Operating Procedure and the Item. 
    '''
    Op = models.ForeignKey(OperatingProcedure)
    Item = models.ForeignKey(Item)

class OperatingProcedure(models.Model):
    '''
    Stores the actual SOP object. 
    '''
    title = model.CharField(max_length = 125)
    date_created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    

    
