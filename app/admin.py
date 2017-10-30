from django.contrib import admin
from .models import Experiment, ExperimentData
# Register your models here.

#~ admin.site.register(Experiment)
#~ admin.site.register(ExperimentData)


class ExperimentDataInline(admin.TabularInline):
    model = ExperimentData
    extra = 0
    
@admin.register(Experiment)
class ExperimentAdmin(admin.ModelAdmin):
    inlines = [ExperimentDataInline]
