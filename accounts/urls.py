from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/',views.login),
    url(r'^register/',views.register),
    url(r'^user/(?P<usr_id>[0-9]+)', views.userpage),
    url(r'^user/', views.profile)
    ]

