from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.ProjectListView.as_view()),
    url(r'^(?P<pk>\d+)/$', views.ProjectUpdateView.as_view()),
    url(r'^create/$', views.ProjectCreateView.as_view()),
    url(r'^delete/(?P<pk>\d+)/$', views.ProjectDeleteView.as_view()),
    url(r'^(?P<project>\d+)/tasks/?$', views.TaskView.as_view()),
    url(r'^(?P<project>\d+)/tasks/(?P<task_id>\d+)/?$', views.TaskView.as_view()),
    url(r'^find_user/$', views.find_user),
    url(r'^calendar/$', views.CalendarTaskView.as_view()),
]
