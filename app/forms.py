from django import forms
from .models import Experiment, ExperimentData
from .models import Template

class csvUpload(forms.Form):
    csv_file = forms.FileField()

class MetadataForm(forms.ModelForm):
    class Meta:
        model = Experiment
        fields = ['person', 'reactor_diameter', 'reactor_length', 
        'num_chambers', 'date','removal_target', 'reactor_age']
         

#~ The default fields in Experiment data.
class ExperimentDataForm(forms.ModelForm):
    class Meta:
        model = ExperimentData
        exclude = ['experiment']
    
    
