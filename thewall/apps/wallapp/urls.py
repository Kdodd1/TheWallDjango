from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^create$', views.create),
	url(r'^login$',views.login),
	url(r'^logged$', views.logged),
	url(r'^message$', views.message),
	url(r'^comment$', views.comment),
	url(r'^deletemessage/(?P<messageid>\d+)$', views.deletemessage),
	url(r'^deletecomment/(?P<commentid>\d+)$', views.deletecomment),
	]