from django import forms

class SettingsForm(forms.Form):
    dateformat = forms.CharField(label="Format to Use for Dates", max_length=10)
    ataglance = forms.CharField(label="At A Glance Data", max_length = 100)
    
