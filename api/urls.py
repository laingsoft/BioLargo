from django.conf.urls import url, include
from . import views
from rest_framework import routers
from rest_framework.authtoken import views as authviews
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
router = routers.DefaultRouter()
router.register(r'comments', views.resttest, 'comment')
router.register(r'tags',views.tags, 'tag')
router.register(r'experiment', views.experiments, 'experiment')
router.register(r'groups', views.groups, 'group')


urlpatterns = [
    url(r'^projects/$', views.projects.as_view(), name="projects"),
    url(r'^getUser', views.get_user),
    url(r'^getToken', obtain_jwt_token),
    url(r'^get_new_token', views.get_new_token),
    url(r'^verifyToken', verify_jwt_token),
    url(r'^', include(router.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^remove/(?P<exp_id>[0-9]+)', views.experimentrm, name="remove_experiment"),
    url(r'^experiment/csv/(?P<exp_id>[0-9]+)', views.get_csv, name='get_csv'),
    url(r'^experimentlist', views.get_experiments_id, name="get_multiple_experiments"),
    url(r'^fields',views.fields_autocomplete, name="fields_autocomplete"),
    url(r'^template', views.templates, name="template"),
    url(r'^comment', views.comment, name="comment"),
    url(r'^testreq', views.requestTest, name="reqtest"),
]
