from django.contrib import admin
from .models import Experiment, ExperimentData, Template, Fields
from django.http import JsonResponse 
from django.conf.urls import url


# Register your models here.

#~ admin.site.register(Experiment)
#~ admin.site.register(ExperimentData)

class ExperimentDataInline(admin.TabularInline):
    model = ExperimentData
    extra = 0
    
@admin.register(Experiment)
class ExperimentAdmin(admin.ModelAdmin):
    inlines = [ExperimentDataInline]

    
@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    change_form_template = 'admin/template_admin.html'
    
    def get_urls(self):
        urls= super().get_urls()
        my_urls = [
            url(r'^add_field/$', self.add_field),
        ]
        
        return my_urls + urls
        
    def add_field(self, request):
        if request.method == "POST":
            name = request.POST.get('field', '')
            if name:
                field = Fields.objects.create(name=name)
                return JsonResponse({'value': field.id, 'text': field.name})
            else:
                return JsonResponse({'success': False, "Error": "No field name given"})
        return JsonResponse({'success': False, "Error": "invalid request"})
        
        
    
