from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.dashboard),
    url(r'^users', views.usermgr),
    url(r'^projects', views.projectmgr),
    url(r'^experiment/($P<exp_id>[0-9]+)', views.experimentmgr),
    url(r'^settings',views.settingsmgr)

    ]
