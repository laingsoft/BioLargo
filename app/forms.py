from django import forms
from .models import Experiment, ExperimentData
from .models import Template
import json

class csvUpload(forms.Form):
    csv_file = forms.FileField()

class uploadForm(forms.ModelForm):
    json = forms.CharField(widget=forms.HiddenInput())
    
    class Meta:
        model = Experiment
        exclude = ['group']
    
    
class GroupsTags(forms.Form):
    group = forms.CharField()
    tags = forms.CharField()
