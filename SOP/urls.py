from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.SOPListView.as_view(), name='sop-list'),
    url(r'^upload/$', views.SOPUploadView.as_view(), name='sop-upload'),
    ]
