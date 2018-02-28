from django import forms
from .models import Task
from accounts.models import Company
from django.contrib.auth import get_user_model


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ('company', 'project', 'complete', 'timestamp', 'related_experiment')

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company')

        super().__init__(*args, **kwargs)
        self.fields['assigned'] = forms.ModelChoiceField(queryset=get_user_model().objects.filter(company=company), required=False)


