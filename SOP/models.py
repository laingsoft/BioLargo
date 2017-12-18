from django.db import models
from inventory.models import Item


class OperatingProcedure(models.Model):
    '''
    Stores the actual SOP object. 
    '''
    title = models.CharField(max_length = 125)
    date_created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    
    
class OpSteps(models.Model):
    '''
    Each individual step that needs to be carried out for 
    the operating procedure. 
    '''
    text = models.CharField(max_length = 1500)
    step_number = models.IntegerField()
    op = models.ForeignKey(OperatingProcedure)

    
class OpMaterials(models.Model):
    '''
    Provides a connection between the Operating Procedure and the Item. 
    '''
    Op = models.ForeignKey(OperatingProcedure)
    Item = models.ForeignKey(Item)

class Calibration(models.Model):
    instrument = models.CharField(max_length = 200)
