from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.cart, name='mycart'),
    url(r'^create_address/$', views.create_address, name='create_address'),
	url(r'^select_address/$', views.select_address, name='select_address'),
	url(r'^checkout/$', views.checkout, name='checkout'),
]