from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^upload/success/(?P<exp_id>[0-9]+)', views.upload_success, name='upload_success'),
    url(r'^upload/form', views.upload_form, name='upload_form'),
    url(r'^upload', views.upload_csv, name = 'upload_csv'),
    url(r'^get_template', views.get_template, name = 'get_template'),
    url(r'^experiment/(?P<exp_id>[0-9]+)', views.experiment, name='experiment'),
    url(r'^experimentjs/(?P<exp_id>[0-9]+)', views.experiment_json, name='experiment_json'),
    url(r'^save_template', views.save_template, name='save_template'),
    url(r'^experiment/csv/(?P<exp_id>[0-9]+)', views.get_csv, name='get_csv'),
    url(r'^fields-autocomplete', views.fields_autocomplete, name='field_autocomplete'),
    url(r'^groups_list', views.groups_list, name='groups_list')
    ]
