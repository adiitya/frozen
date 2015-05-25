from django.conf.urls import url

urlpatterns = [
    url(),
]
urlpatterns = [
	url(r'^$', IndexView.as_view(), name = 'index'),
	url(r'^(?P<pk>[0-9]+)/$', DetailView.as_view(), name='details'),
	url(r'^(?P<pk>[0-9]+)/result/$',ResultView.as_view(), name='result'),
	url(r'^(?P<ques_id>[0-9]+)/vote/$', vote, name='vote'),
]