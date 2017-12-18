from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.dashboard),
    url(r'^users', views.usermgr),
    url(r'^projects', views.projectmgr),
    url(r'^experiment/($P<exp_id>[0-9]+)', views.experimentmgr),
    url(r'^settings', views.settingsmgr),
    url(r'^templates/$', views.TemplateListView.as_view(), name='template-list'),
    url(r'^templates/create/$', views.TemplateCreateView.as_view()),
    url(r'^templates/edit/(?P<pk>\d+)/$', views.TemplateUpdateView.as_view()),
    url(r'^fields/$', views.FieldListView.as_view(), name='template-list'),
    url(r'^fields/create/$', views.FieldCreateView.as_view()),
    url(r'^fields/edit/(?P<pk>\d+)/$', views.FieldUpdateView.as_view()),
    ]
