from django.contrib import admin
from .models import Experiment, ExperimentData
# Register your models here.

admin.site.register(Experiment)
admin.site.register(ExperimentData)
