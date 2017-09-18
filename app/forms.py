from django import forms

class csvUpload(forms.form):
    csv_file = forms.FileField()
