from django.conf.urls import url
from . import views

urlpatterns=[
	url(r'^$', views.preindex),
	url(r'^main$', views.index),
	url(r'^register$', views.register),
	url(r'^login$', views.login),
	url(r'^travels$', views.travels),
	url(r'^logout$', views.logout),
	url(r'^join/(?P<id>\d+)$', views.join),
	url(r'^travels/add$', views.add),
	url(r'^addTrip$', views.addTrip),
	url(r'^travels/destination/(?P<id>\d+)$', views.destination)
]