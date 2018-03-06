from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.SOPListView.as_view()),
    url(r'^upload/$', views.SOPUploadView.as_view()),
    url(r'^download/(?P<file_id>[0-9]+)$', views.SOPDownloadView),
    url(r'^(?P<pk>[0-9]+)$', views.SOPUpdateView.as_view()),
    url(r'^find/$', views.findSOP),
    ]

