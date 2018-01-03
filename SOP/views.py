from django.shortcuts import render
from SOP.models import *
from django.views.generic import ListView
# Create your views here.

class StandardOperatingProcedure(ListView):
    model = OperatingProcedure
    
