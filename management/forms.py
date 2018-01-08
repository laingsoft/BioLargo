from django import forms
from app.models import Fields, Template

class SettingsForm(forms.Form):
    dateformat = forms.CharField(label="Format to Use for Dates", max_length=10)
    ataglance = forms.CharField(label="At A Glance Data", max_length = 100)


class TemplateForm(forms.ModelForm):
    """
    Form used to add and edit templates in management panel.
    """
    class Meta:
        model = Template
        exclude = ('company',)


class FieldForm(forms.ModelForm):
    """
    Form used to add and edit fields in management panel.
    """

    class Meta:
        model = Fields
        exclude = ('company',)

