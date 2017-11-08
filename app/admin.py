from django.contrib import admin
from .models import Experiment, ExperimentData, Template, Fields
from .models import Tag, Group, Comment
from django.http import JsonResponse 
from django.conf.urls import url
from django import forms
from .forms import ModelSuggestField, ModelMultipleSuggestField


# Register your models here.

#~ admin.site.register(Experiment)
#~ admin.site.register(ExperimentData)

# Widget used to enter and edit metadata. Creates individual form fields for 
# each metadata field given a list of metadata fields. Compress returns a dict
# with the metadata field names as the keys.
class MetadataWidget(forms.MultiValueField):
    def _init_(self, *args, **kwargs):
        try:
            metadata_field = kwargs.pop('metadata_fields')
        except KeyError:
            raise ValueError("No metadata fields given")

        empty_value = kwargs.get("empty_value", 'e')

        fields = []

        for field in metadata_fields:
            fields.append(forms.CharField(label = field, empty_value = 
                empty_value, strip =True))

        super()._init_(fields = fields , require_all_fields = False, *args,  
            **kwargs)

    def compress(data_list):
        return dict(zip(self.metadata_fields, data_list))

# custom form for editng and adding experiments (excluding experiment data and
# comments). Experiment data and comments are added/edited via inlines. 
class ExperimentForm(forms.ModelForm):
    group = ModelSuggestField(Group.objects.all(), Group, to_field_name="name")
    tags = ModelMultipleSuggestField(Tag.objects.all(), Tag, to_field_name="name", required=False)
    class Meta:
        model = Experiment
        fields = ["friendly_name", "metadata"]


    def __init__(self, *args, **kwargs):
        try:
            metadata_fields = kwargs.pop('metadata_fields')
        except KeyError:
            raise ValueError("No metadata fields given")

        self.fields['metadata'].widget = MetadataWidget(metadata_fields = metadata_fields)
  
# experiment data inline. Renders each field as a MultivalueField then entire 
# inline as a table
class ExperimentDataInline(admin.TabularInline):
    model = ExperimentData
    extra = 0


# ModelAdmin for Experiments     
@admin.register(Experiment)
class ExperimentAdmin(admin.ModelAdmin):
    inlines = [ExperimentDataInline]



# Form used for editing and creating templates.
# Uses the ModelMultipleSuggestionField to csuggest and create fields. 
# Replaces the original ajax calls for creating fields.
class TemplateForm(forms.ModelForm):
    fields =  ModelMultipleSuggestField(Fields.objects.all(), Fields, to_field_name="name")
    
    class Meta:
        model = Template
        exclude = []

               
@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    change_form_template = 'admin/template_admin.html'
    form = TemplateForm
    
    # def get_urls(self):
    #     urls= super().get_urls()
    #     my_urls = [
    #         url(r'^add_field/$', self.add_field),
    #     ]
        
    #     return my_urls + urls
        
    # def add_field(self, request):
    #     if request.method == "POST":
    #         name = request.POST.get('field', '')
    #         if name:
    #             field = Fields.objects.create(name=name)
    #             return JsonResponse({'value': field.id, 'text': field.name})
    #         else:
    #             return JsonResponse({'success': False, "Error": "No field name given"})
    #     return JsonResponse({'success': False, "Error": "invalid request"})
        
        
    
