from django.conf.urls import url
from . import views
from inventory.views import ItemList, ItemCreate, ItemDetail

urlpatterns = [
    url(r'^$',ItemList.as_view()),
    url(r'^add', ItemCreate.as_view()),
    url(r'^item/(?P<pk>[0-9]+)', ItemDetail.as_view())
    ]
