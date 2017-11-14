from django.contrib import admin
from .models import Experiment, ExperimentData, Template, Fields
from .models import Tag, Group, Comment
from django.http import JsonResponse 
from django.conf.urls import url
from django import forms
from .forms import ModelSuggestField, ModelMultipleSuggestField
from django.forms import ModelForm


# a placeholder while organization settings have not been implemented.
METADATA_FIELDS = ["Reactor Diameter [inch]","Reactor Length [inch]", 
"#Chambers", "Date (d/m/y)", "Removal Target", "Age of reactor [L]"] 

#~ admin.site.register(Experiment)
#~ admin.site.register(ExperimentData)
admin.site.register(Group)


class JSONWidget(forms.MultiWidget):
    template_name = "widgets/JSONWidget.html"

    def __init__(self, *args, **kwargs):
        self.template = kwargs.pop('template')

        widgets = []

        for item in self.template:
            widgets.append(forms.TextInput(attrs={'title': item, 'placeholder':item}))

        super().__init__(widgets = widgets, *args, **kwargs)

    def decompress(self, value):
        if value:
            values_list = []

            for item in self.template:
                values_list.append(value[item])
            return values_list
            
        return ''


# form field used to enter and edit metadata. Creates individual form fields for 
# each metadata field given a list of metadata fields. Compress returns a dict
# with the metadata field names as the keys.
class JSONField(forms.MultiValueField):

    def __init__(self, *args, **kwargs):
        try:
            self.template = kwargs.pop("template")
        except KeyError:
            raise ValueError("Missing metadata template")

        empty_value = kwargs.pop("empty_value", 'e')

        fields = []

        for field in self.template:
            fields.append(forms.CharField(label=field))

        super().__init__(fields = fields , require_all_fields = False, *args, **kwargs)

        self.widget = JSONWidget(template = self.template)

    def compress(self, data_list):
        return dict(zip(self.template, data_list))

# custom form for editng and adding experiments (excluding experiment data and
# comments). Experiment data and comments are added/edited via inlines. 
class ExperimentForm(forms.ModelForm):
    group = ModelSuggestField(Group.objects.all(), Group, 
        to_field_name = "name")
    tags = ModelMultipleSuggestField(Tag.objects.all(), Tag, 
        to_field_name = "name", required = False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        template = METADATA_FIELDS # for now. get the template from current user later.
        self.fields['metadata'] = JSONField(template = template)


class ExperimentDataForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.experimentData:
            # print(self.instance)
            template = self.instance.experimentData.keys()

        else:
            template = Template.objects.all().values_list( "fields__name" , flat = True) # TODO: UPDATE TO USE THE PROPER TEMPLATE

        self.fields['experimentData'] = JSONField(template = template)

  
# experiment data inline. Renders each field as a MultivalueField then entire 
# inline as a table
class ExperimentDataInline(admin.TabularInline):
    template = "admin/experiment_inline.html"
    form = ExperimentDataForm
    model = ExperimentData
    extra = 0


# ModelAdmin for Experiments     
@admin.register(Experiment)
class ExperimentAdmin(admin.ModelAdmin):
    inlines = [ExperimentDataInline]
    form = ExperimentForm

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.current_user = request.user
        return form
        
    
# Form used for editing and creating templates.
# Uses the ModelMultipleSuggestionField to csuggest and create fields. 
# Replaces the original ajax calls for creating fields.
class TemplateForm(forms.ModelForm):
    fields =  ModelMultipleSuggestField(Fields.objects.all(), Fields, 
        to_field_name="name")
    
               
@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    change_form_template = 'admin/template_admin.html'
    form = TemplateForm
    