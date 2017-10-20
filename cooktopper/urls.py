from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.homepage, name='HomePage'),
	url(r'^Burner(?P<id>\d+)/$', views.burner, name='burner'),
	url(r'^register/$', views.register, name='register')
]
