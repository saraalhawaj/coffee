from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^pay/(?P<order_id>\d+)/$', views.pay, name='pay'),

    ]