from django import forms

class csvUpload(forms.Form):
    csv_file = forms.FileField()
