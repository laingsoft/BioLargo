from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^$', login_required(views.SOPListView.as_view())),
    url(r'^upload/$',login_required(views.SOPUploadView.as_view())),
    url(r'^download/(?P<file_id>[0-9]+)$', login_required(views.SOPDownloadView)),
    url(r'^(?P<pk>[0-9]+)$', login_required(views.SOPUpdateView.as_view())),
    url(r'^find/$', login_required(views.findSOP)),
    ]

