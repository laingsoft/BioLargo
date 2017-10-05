from django import forms
from .models import Experiment, ExperimentData
from .models import Template
from .models import Tag, Group
import json
from django.core.exceptions import ValidationError
from django.utils.encoding import force_text

# custom choice fields for suggesting models/

class ModelSuggestField(forms.ModelChoiceField):
    def __init__(self, queryset, model, to_field_name=None):
        super(ModelSuggestField, self).__init__(queryset, to_field_name=to_field_name)
        self.model = model

    def to_python(self, value):
            if value in self.empty_values:
                return None
            try:
                key = self.to_field_name or 'pk'
                value = self.queryset.get(**{key: value})
            except (ValueError, self.queryset.model.DoesNotExist):
                if value and value != "":
                    value = self.model(name=value)
                    value.save()
                else: 
                    raise ValidationError(self.error_messages['invalid_choice'], code='invalid_choice')
            print(value)
            return value

class ModelMultipleSuggestField(forms.ModelMultipleChoiceField):
    def __init__(self, queryset, model, to_field_name=None):
        super(ModelMultipleSuggestField, self).__init__(queryset, to_field_name=to_field_name)
        self.model = model
        
        
    def clean(self, value):
        if self.required and not value:
            raise ValidationError(self.error_messages['required'])
        elif not self.required and not value:
            return []
        if not isinstance(value, (list, tuple)):
            raise ValidationError(self.error_messages['list'])
        key = self.to_field_name or 'pk'
        for pk in value:
            try:
                self.queryset.filter(**{key: pk})
            except (ValueError, self.queryset.model.DoesNotExist):
                obj = self.model(name = pk)
                obj.save()
                
        qs = self.queryset.filter(**{'%s__in' % key: value})
        pks = set([force_text(getattr(o, key)) for o in qs])
        for val in value:
            if force_text(val) not in pks:
                raise ValidationError(self.error_messages['invalid_choice'] % val)

        self.run_validators(value)
            
        return qs

class csvUpload(forms.Form):
    csv_file = forms.FileField()

class uploadForm(forms.ModelForm):
    json = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Experiment
        exclude = ['group']


class GroupsTags(forms.Form):
    group = ModelSuggestField(Group.objects.all(), Group, to_field_name="name")
    tags = ModelMultipleSuggestField(Tag.objects.all(), Tag, to_field_name="name")
