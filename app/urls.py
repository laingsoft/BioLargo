from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^upload/csv', views.csv_upload, name='upload csv'),
    url(r'^upload/success/(?P<id>[0-9]+/$)', views.upload_success),
    url(r'^experiment/(?P<id>[0-9]+/$)', views.experiment),
    ]
