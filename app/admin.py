from django.contrib import admin
from .models import Experiment, ExperimentData, Template, Fields


# Register your models here.

#~ admin.site.register(Experiment)
#~ admin.site.register(ExperimentData)

class ExperimentDataInline(admin.TabularInline):
    model = ExperimentData
    extra = 0
    
@admin.register(Experiment)
class ExperimentAdmin(admin.ModelAdmin):
    inlines = [ExperimentDataInline]


class FieldsInline(admin.TabularInline):
    model = Template.fields.through
    extra = 0
    
@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    exclude = ['fields']
    inlines = [FieldsInline]
