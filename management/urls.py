from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.dashboard),
    url(r'^projects/$', views.ProjectListView.as_view()),
    url(r'^projects/edit/(?P<pk>\d+)/$', views.ProjectUpdateView.as_view()),
    url(r'^projects/create/$', views.ProjectCreateView.as_view()),
    url(r'^projects/delete/(?P<pk>\d+)/$', views.ProjectDeleteView.as_view()),
    url(r'^settings', views.SettingsUpdateView.as_view()),
    url(r'^templates/$', views.TemplateListView.as_view()),
    url(r'^templates/create/$', views.TemplateCreateView.as_view()),
    url(r'^templates/edit/(?P<pk>\d+)/$', views.TemplateUpdateView.as_view()),
    url(r'^templates/delete/(?P<pk>\d+)/$', views.TemplateDeleteView.as_view()),
    url(r'^fields/$', views.FieldListView.as_view()),
    url(r'^fields/create/$', views.FieldCreateView.as_view()),
    url(r'^fields/edit/(?P<pk>\d+)/$', views.FieldUpdateView.as_view()),
    url(r'^experiments/$', views.ExperimentListView.as_view()),
    url(r'^experiments/edit/(?P<pk>\d+)/$', views.ExperimentUpdateView.as_view()),
    url(r'^experiments/delete/(?P<pk>\d+)/$', views.ExperimentDeleteView.as_view()),
    url(r'^users/$', views.UserListview.as_view()),
    url(r'^users/edit/(?P<pk>\d+)/$', views.UserUpdateView.as_view()),
    ]
