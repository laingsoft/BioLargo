from django.conf.urls import url, include
from . import views
from project_management.views import UserTaskListView, task_complete
import analytics.urls

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^upload/success/(?P<exp_id>[0-9]+)', views.upload_success, name='upload_success'),
    url(r'^upload', views.upload, name = 'upload'),
    url(r'^get_template', views.get_template, name = 'get_template'),
    url(r'^experiments/$', views.ExperimentListView.as_view(), name='experiment_list_view'),
    url(r'^experiment/(?P<pk>[0-9]+)/$', views.ExperimentDetailView.as_view(), name='experiment'),
    url(r'^experiment/images/$', views.ExperimentImageUploadView),
    url(r'^experimentjs/(?P<exp_id>[0-9]+)', views.experiment_json, name='experiment_json'),
    url(r'^experimentrm/(?P<exp_id>[0-9]+)', views.experimentrm, name="experimentrm"),
    url(r'^experiment/csv/(?P<exp_id>[0-9]+)', views.get_csv, name='get_csv'),
    url(r'^projects/(?P<pk>[0-9]+)/$', views.ProjectDetailView.as_view(), name="project_page"),
    url(r'^projects/$', views.ProjectListView.as_view(), name="project_list"),
    url(r'^create_tag/$', views.create_tag, name="create_tag"),
    url(r'^watch/$', views.watch, name="watch"),
    url(r'^experiments/watched', views.WatchedExperimentListView.as_view()),
    url(r'^projects/watched', views.WatchedProjectsListView.as_view()),
    url(r'^notif_read/$', views.notif_read),
    url(r'^tasks/$', UserTaskListView.as_view()),
    url(r'^task_complete/(?P<id>[0-9]+)/?$', task_complete),
    url(r'^analysis/', include(analytics.urls))
    ]
