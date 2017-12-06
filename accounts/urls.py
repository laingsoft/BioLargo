from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^login/$', auth_views.LoginView.as_view(redirect_authenticated_user =  True)),
    # url(r'^register/', views.register, name="register"),
    # url(r'^user/(?P<usr_id>[0-9]+)', views.userpage),
    # url(r'^profile/', views.profile),
    # url(r'^userlist/', views.userlist),
    # url(r'^messages/', views.messaging),
    url(r'^logout/$', auth_views.logout_then_login ),
    url(r'^register/$', views.company_register)
    ]