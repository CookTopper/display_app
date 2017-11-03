from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.homepage, name='HomePage'),
	url(r'^burner/(?P<id>\d+)/$', views.burner, name='burner'),
	url(r'^program_burner/(?P<id>\d+)/$', views.burner, name='program_burner'),
]
