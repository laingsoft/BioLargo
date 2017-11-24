from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^experiment/(?P<exp_id>[0-9]+)', views.get_experimentbyid, name='experiment_json'),
    url(r'^remove/(?P<exp_id>[0-9]+)', views.experimentrm, name="remove_experiment"),
    url(r'^experiment/csv/(?P<exp_id>[0-9]+)', views.get_csv, name='get_csv'),
    url(r'^experimentlist', views.get_experiments_id, name="get_multiple_experiments"),
    url(r'^groups', views.groups_list, name="groups_list"),
    url(r'^fields',views.fields_autocomplete, name="fields_autocomplete"),
    url(r'^template', views.templates, name="template"),
    url(r'^comment', views.comment, name="comment")
]
