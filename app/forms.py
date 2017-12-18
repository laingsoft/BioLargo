from django import forms
from .models import Template
from .models import Tag, Project, Experiment


class ExperimentDataForm(forms.Form):
    """
    Form that accepts JSON with experiement data and metadata
    """
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


class ExperimentForm(forms.ModelForm):
    """
    model form for base experiment information. Metadata is added  later by
    with data from the ExperimentDataForm. Sends template used along with
    the json.
    """
    class Meta:
        model = Experiment
        fields = ('friendly_name', 'project', 'tags',)
        widgets = {'friendly_name': forms.TextInput(attrs={'class': 'form-control'}), }

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
    """
    Form for creating projects. Will be removed in a later refactor switching
    to class based generic views for lists, adding and updating.
    """
    class Meta:
        model = Project
        exclude = ('company', )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'start': forms.TextInput(attrs={'class': 'form-control'}),
            'end': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
