from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.ProjectListView.as_view()),
    url(r'^(?P<pk>\d+)/$', views.ProjectDetailView.as_view()),
    url(r'^edit/(?P<pk>\d+)/$', views.ProjectUpdateView.as_view()),
    url(r'^create/$', views.ProjectCreateView.as_view()),
    url(r'^delete/(?P<pk>\d+)/$', views.ProjectDeleteView.as_view()),
    url(r'^tasks/(?P<project>\d+)/$', views.tasks),
]
