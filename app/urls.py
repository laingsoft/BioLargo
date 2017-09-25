from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^upload/success/(?P<exp_id>[0-9]+)', views.upload_success),
    url(r'^upload/form', views.upload_form),
    url(r'^upload', views.upload_csv),
    url(r'^get_template', views.get_template),
    ]
