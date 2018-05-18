from django.conf.urls import url
from . import views
from inventory.views import ItemList, ItemCreate, ItemDetail
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$',login_required(ItemList.as_view())),
    url(r'^add', login_required(ItemCreate.as_view())),
    url(r'^item/(?P<pk>[0-9]+)',login_required(ItemDetail.as_view()))
    ]
