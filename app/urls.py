from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^upload/success/(?P<exp_id>[0-9]+)', views.upload_success, name='upload_success'),
    url(r'^upload', views.upload, name = 'upload'),
    url(r'^get_template', views.get_template, name = 'get_template'),
    url(r'^experiments/$', views.ExperimentListView.as_view(), name='experiment_list_view'),
    url(r'^experiment/(?P<exp_id>[0-9]+)', views.experiment, name='experiment'),
    url(r'^experimentjs/(?P<exp_id>[0-9]+)', views.experiment_json, name='experiment_json'),
    url(r'^experimentrm/(?P<exp_id>[0-9]+)', views.experimentrm, name="experimentrm"),
    url(r'^experiment/csv/(?P<exp_id>[0-9]+)', views.get_csv, name='get_csv'),
    url(r'^analysis', views.analysis_page, name='analysis_page'),
    url(r'^experiments_list', views.experiments_list, name="experiments_list"),
    url(r'^projects/(?P<p_id>[0-9]+)/$', views.project_page, name="project_page"),
    url(r'^projects/$', views.project_list, name="project_list"),
    url(r'^projects/create/$', views.create_project, name="create_project"),
    url(r'^create_tag/$', views.create_tag, name="create_tag"),

    ]
