from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^login/$', views.user_login, name='login'),
  url(r'^status/$', views.ip_status, name='status'),
  url(r'^settings/$', views.user_settings, name='settings'),
  url(r'^logout/$', views.user_logout, name='logout'),
  url(r'^add_ip/$', views.add_ip, name='addIp'),
  url(r'^delete_ip/$', views.delete_ip, name='deleteIp'),
  url(r'^list_ip/$', views.get_ip_by_user, name='listIp'),
  url(r'^$', views.index, name='home'),
]