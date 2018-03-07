from django.conf.urls import url, include
from . import views
from rest_framework import routers
from rest_framework.authtoken import views as authviews
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
router = routers.DefaultRouter()
router.register(r'tags', views.tags, 'tag')
router.register(r'experiment', views.experiments, 'experiment')


urlpatterns = [
    url(r'^sop/$', views.get_sop),
    url(r'^get_tasks/(?P<task_status>[N,C,I])/(?P<page>[0-9]+)/$', views.get_tasks),
    url(r'^task_in_progress/(?P<id>[0-9]+)$', views.mark_task_in_progress),
    url(r'^task_complete/(?P<id>[0-9]+)$', views.mark_task_complete),
    url(r'^analysis/', views.analysis_page),
    url(r'^read_notification/(?P<id>[0-9]+)$', views.read_notification),
    url(r'^toggle_watch/$', views.watch),
    url(r'^overview_count/$', views.get_overview_count),
    url(r'^tags/$', views.tags.as_view()),
    url(r'^experiment_data/(?P<id>[0-9]+)$', views.get_experiment_data),
    url(r'^experiments_with_project_id/(?P<id>[0-9]+)/(?P<page>[0-9]+)$', views.get_experiments_with_project_id, name="experiments_with_project_id"),
    url(r'^experiments_with_experiment_id/(?P<id>[0-9]+)$', views.get_experiments_with_experiment_id, name="experiments_with_experiment_id"),
    url(r'^experiments/delete/(?P<id>[0-9]+)/$', views.experiments_delete),
    url(r'^experiments/(?P<page>[0-9]+)/$', views.experiments.as_view()),
    url(r'^project_stats/(?P<id>[0-9]+)$', views.get_project_stats),
    url(r'^projects/delete/(?P<id>[0-9]+)/$', views.projects_delete),
    url(r'^projects/(?P<page>[0-9]+)/$', views.projects.as_view()),
    url(r'^get_company_users/$', views.get_company_users),
    url(r'^get_user', views.get_user),
    url(r'^get_token', obtain_jwt_token),
    url(r'^get_new_token', views.get_new_token),
    url(r'^verifyToken', verify_jwt_token),
    url(r'^', include(router.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^templates/(?P<id>[0-9]+)$', views.template.as_view(), name="template"),
    url(r'^templates/$', views.template.as_view(), name="templates"),
    url(r'^comment/(?P<id>[0-9]+)$', views.comment.as_view()),
    url(r'^comment/$', views.comment.as_view()),
]
