from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^upload/success/(?P<exp_id>[0-9]+)', views.upload_success, name='upload_success'),
    url(r'^upload_form', views.upload_form, name ='upload_form'),
    url(r'^upload_file', views.upload_file, name = 'upload_file' ),
    url(r'^upload', views.upload, name = 'upload'),
    url(r'^get_template', views.get_template, name = 'get_template'),
    url(r'^experiment/(?P<exp_id>[0-9]+)', views.experiment, name='experiment'),
    url(r'^experimentjs/(?P<exp_id>[0-9]+)', views.experiment_json, name='experiment_json'),
    url(r'^experimentrm/(?P<exp_id>[0-9]+)', views.experimentrm, name="experimentrm"),
    url(r'^save_template', views.save_template, name='save_template'),
    url(r'^experiment/csv/(?P<exp_id>[0-9]+)', views.get_csv, name='get_csv'),
    url(r'^fields-autocomplete', views.fields_autocomplete, name='field_autocomplete'),
    url(r'^analysis', views.analysis_page, name = 'analysis_page'),
    url(r'^experiments_list', views.experiments_list, name="experiments_list"),
    ]
