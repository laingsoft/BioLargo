"""PredoxWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from app.views import serve_image
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet

urlpatterns = [
    url(r'^devices/', FCMDeviceAuthorizedViewSet.as_view({'post':'create', 'get':'list'}), name='create_fcm_device'),
    url(r'^admin/', admin.site.urls),
    url(r'^app/', include('app.urls')),
    url(r'^accounts/',include('accounts.urls')),
    url(r'^', include('frontpage.urls')),
    url(r'^api/',include('api.urls')),
    url(r'api-token-auth/', obtain_jwt_token),
    url(r'api-token-refresh/', refresh_jwt_token),
    url(r'management/',include('management.urls')),
    url(r'inventory/', include('inventory.urls')),
    url(r'sop/', include('SOP.urls')),
    url(r'management/projects/', include('project_management.urls')),
    url(r'^user_images/', serve_image),
]
