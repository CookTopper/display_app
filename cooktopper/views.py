from django.shortcuts import render
from .models import Stove, BurnerState, Temperature, Burner, PanState, Pan, ProgrammingType, ProgrammingDetails, Programming, Shortcut
import requests
import json
import time

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

class WebServiceBurnerState():
	def __init__(self, id):
		self.id = id
		self.url = 'http://localhost:8000/burner_state/?id=' + str(id)
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
		burner_state_id = self.request_json[0].get('burner_state')
		return burner_state_id

	def burner_state(self):
		web_service_burner_state = WebServiceBurnerState(self.burner_state_id())
		burner_state_description = web_service_burner_state.description()
		return BurnerState.objects.get(description=burner_state_description)

class RequestBurner():
	def get_requests(self, url):
		request_result = requests.get(url)
		request_json = request_result.json()
		return request_json

	def check_request(self, request):
		tolerance = 5
		return int(time.time()) - int(request['time']) < tolerance

	def update_burners(self, url):
		requests = self.get_requests(url)

		for request in requests:
			if (self.check_request(request)):
				burner_web_service_id = request['burner_id']
				temperature_web_service_id = request['new_temperature']
				burner_state_web_service_id = request['new_burner_state']

				web_service_burner = WebServiceBurner(burner_web_service_id)
				burner_description = web_service_burner.description()
				burner = Burner.objects.get(description=burner_description)

				web_service_temperature = WebServiceTemperature(temperature_web_service_id)
				temperature_description = web_service_temperature.description()
				new_temperature = Temperature.objects.get(description=temperature_description)

				web_service_burner_state = WebServiceBurnerState(burner_state_web_service_id)
				burner_state_description = web_service_burner_state.description()
				new_burner_state = BurnerState.objects.get(description=burner_state_description)

				burner.temperature = new_temperature
				burner.burner_state = new_burner_state

				burner.save()

			#self.delete_request(request['id'])

	def delete_request(self, request_id):
		requests.delete('http://localhost:8000/request_burner/' + str(request_id))

def homepage(request):
	request_burner_url = 'http://localhost:8000/request_burner/'

	request_burner = RequestBurner()
	request_json = request_burner.get_requests(request_burner_url)

	request_burner.update_burners(request_burner_url)

	burners = Burner.objects.all()

	return render(request, 'cooktopper/index.html', {'burners': burners})

def burner(request, id):
	burner = Burner.objects.get(pk=id)
	return render(request, 'cooktopper/burner.html', {'burner': burner})
