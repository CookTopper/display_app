from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.homepage, name='HomePage'),
	url(r'^burner/(?P<id>\d+)/$', views.burner, name='burner'),
	url(r'^program_burner/(?P<burner_id>\d+)/$', views.program_burner, name='program_burner'),
	url(r'^register/$', views.register, name='register'),
	url(r'^server_burner/$', views.server_burner),
	url(r'^scale/$', views.scale)
]
