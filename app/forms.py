from django import forms
from .models import Template
from .models import Tag, Project


class ExperimentForm(forms.Form):
    json = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        try:
            company = kwargs.pop("company")
        except KeyError:
            raise ValueError("Missing company argument")

        super().__init__(*args, **kwargs)

        self.fields["template"] = forms.ModelChoiceField(
            queryset=Template.objects.filter(company=company),
            to_field_name='name')


class FileUpload(forms.Form):
    upload_file = forms.FileField(label='Select file to upload')


class ProjectTags(forms.Form):

    def __init__(self, *args, **kwargs):
        try:
            company = kwargs.pop('company')
        except KeyError:
            raise ValueError("Missing company argument")

        super().__init__(*args, **kwargs)

        self.fields['project'] = forms.ModelChoiceField(
            queryset=Project.objects.filter(company=company),
            to_field_name='name')

        self.fields['tags'] = forms.ModelMultipleChoiceField(
            queryset=Tag.objects.filter(company=company),
            to_field_name='name')


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ('company', )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'start': forms.TextInput(attrs={'class': 'form-control'}),
            'end': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
