from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'pricing/$', views.pricing),
    url(r'contactus/$', views.contactus),
    url(r'support/$', views.support),
    url(r'features/$', views.features),
    url(r'invest/$', views.invest)
    ]
