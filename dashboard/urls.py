from django.conf.urls import url

from . import views
urlpatterns = [
    url(r'^add_ip/$', views.add_ip, name='addIp'),
    url(r'^delete_ip/$', views.delete_ip, name='deleteIp'),
]