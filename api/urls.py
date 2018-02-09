from django.conf.urls import url, include
from . import views
from rest_framework import routers
from rest_framework.authtoken import views as authviews
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
router = routers.DefaultRouter()
router.register(r'comments', views.resttest, 'comment')
router.register(r'tags', views.tags, 'tag')
router.register(r'experiment', views.experiments, 'experiment')


urlpatterns = [
    url(r'^toggle_watch/$', views.watch),
    url(r'^overview_count/$', views.getOverviewCount),
    url(r'^tags/$', views.tags.as_view()),
    url(r'^experiment_data/(?P<id>[0-9]+)$', views.getExperimentData),
    url(r'^experiments_with_project_id/(?P<id>[0-9]+)$', views.getExperimentsWithProjectId, name="experiments_with_project_id"),
    url(r'^experiments/(?P<id>[0-9]+)$', views.experiments.as_view(), name="delete_experiment"),
    url(r'^experiments/$', views.experiments.as_view(), name="experiments"),
    url(r'^projects/(?P<id>[0-9]+)$', views.projects.as_view(), name="delete_project"),
    url(r'^projects/$', views.projects.as_view(), name="projects"),
    url(r'^getUser', views.get_user),
    url(r'^getToken', obtain_jwt_token),
    url(r'^get_new_token', views.get_new_token),
    url(r'^verifyToken', verify_jwt_token),
    url(r'^', include(router.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^fields',views.fields_autocomplete, name="fields_autocomplete"),
    url(r'^templates/(?P<id>[0-9]+)$', views.template.as_view(), name="template"),
    url(r'^templates/$', views.template.as_view(), name="templates"),
    url(r'^comment/', views.comment, name="comment"),
    url(r'^comments/(?P<id>[0-9]+)$', views.get_exp_comments),
    url(r'^testreq', views.requestTest, name="reqtest"),
]
