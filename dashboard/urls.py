from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^login/$', views.user_login, name='login'),
  url(r'^settings/$', views.user_settings, name='settings'),
  url(r'^logout/$', views.user_logout, name='logout'),
]