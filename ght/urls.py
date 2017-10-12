from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^gpio/(?P<pk>\d+)/$', views.led, name='led'),
    url(r'^gpio/(?P<pk>\d+)/$', views.audio, name='audio'),
]  