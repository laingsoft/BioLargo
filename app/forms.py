from django import forms
from .models import Experiment, ExperimentData
from .models import Template

class csvUpload(forms.Form):
    #~ group = forms.CharField()
    csv_file = forms.FileField()

class MetadataForm(forms.ModelForm):
    class Meta:
        model = Experiment
        exclude = ['group']
        #~ widgets = {'group' : forms.TextInput()}
         

#~ The default fields in Experiment data.
class ExperimentDataForm(forms.Form):
    json = forms.CharField(widget=forms.HiddenInput())
        
    
    
class UploadExtra(forms.Form):
    group = forms.CharField()
    tags = forms.CharField(widget=forms.HiddenInput())
