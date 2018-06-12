from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^login/$', auth_views.LoginView.as_view(redirect_authenticated_user =  True)),
    url(r'^user/(?P<usr_id>[0-9]+)', views.userpage),
    url(r'^profile/', views.profile),
    url(r'^userlist/', views.userlist),
    url(r'^messages/', views.messaging),
    url(r'^logout/$', auth_views.logout_then_login ),
    url(r'^register/$', views.company_register),
    url(r'^invite/(?P<linkHash>[\w\W]+)', views.register_user),
    url(r'^invite/', views.generate_invite),
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
]
