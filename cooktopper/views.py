from django.shortcuts import render
from .models import Stove, BurnerState, Temperature, Burner, PanState, Pan, ProgrammingType, ProgrammingDetails, Programming, Shortcut
import requests
import json

class WebServiceTemperature():
	def __init__(self, id):
		self.id = id
		self.url = 'http://localhost:8000/temperature/?id=' + str(id)
		self.request_result = requests.get(self.url)
		self.request_json = self.request_result.json()
		self.request_text = self.request_result.text

	def description(self):
		description = self.request_json[0].get('description')
		return description

class WebServiceBurner():
	def __init__(self, id):
		self.id = id
		self.url = 'http://localhost:8000/burner/?id=' + str(id)
		self.request_result = requests.get(self.url)
		self.request_json = self.request_result.json()
		self.request_text = self.request_result.text

	def description(self):
		description = self.request_json[0].get('description')
		return description

	def stove_id(self):
		pass

	def temperature_id(self):
		temperature_id = self.request_json[0].get('temperature')
		return temperature_id

	def temperature(self):
		web_service_temperature = WebServiceTemperature(self.temperature_id())
		temperature_description = web_service_temperature.description()
		return Temperature.objects.get(description=temperature_description)

	def burner_state_id(self):
		pass

class RequestBurner():
#	def create(self, url):
#		self.request_result = requests.get(url)
#		self.request_list_json = request_result.json()

	def get_requests(self, url):
		request_result = requests.get(url)
		request_json = request_result.json()
		return request_json

	def check_request(self, request):
		#Put here the logic to check if too much time has passed
		return True 

	def update_burners(self, url):
		requests = self.get_requests(url)

		for request in requests:
			if (self.check_request(request)):
				burner_web_service_id = request['burner_id']
				web_service_burner = WebServiceBurner(burner_web_service_id)
				burner_description = web_service_burner.description()

				burner = Burner.objects.get(description=burner_description)
				burner.temperature = web_service_burner.temperature()

				burner.save()

				#delete request here

	def delete_request(request_id):
		#Put here the logic to delete a RequestBurner request
		pass

def homepage(request):
	request_burner_url = 'http://localhost:8000/request_burner/'

	request_burner = RequestBurner()
	request_json = request_burner.get_requests(request_burner_url)

	request_burner.update_burners(request_burner_url)

	burners = Burner.objects.all()

	return render(request, 'cooktopper/index.html', {'burners': burners, 'request_json': request_json})

def burner(request, id):
	burner = Burner.objects.get(pk=id)
	return render(request, 'cooktopper/burner.html', {'burner': burner})
