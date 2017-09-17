from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index2/(?P<pk>\d+)/$', views.index2, name='index2'),
]