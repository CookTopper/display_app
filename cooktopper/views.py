from django.shortcuts import render
from .models import Stove, BurnerState, Temperature, Burner, PanState, Pan, ProgrammingType, ProgrammingDetails, Programming, Shortcut
import requests
import json
import time

class WebServiceTemperature():
	def __init__(self, id=None, description=None):
		if id is not None:
			self.url = 'http://localhost:8000/temperature/?id=' + str(id)
		elif description is not None:
			self.url = 'http://localhost:8000/temperature/?description=' + str(description)
		else:
			#Invalid Option
			pass

		self.request_result = requests.get(self.url)
		self.request_json = self.request_result.json()
		self.request_text = self.request_result.text

	def id(self):
		id = self.request_json[0].get('id')
		return id

	def description(self):
		description = self.request_json[0].get('description')
		return description

class WebServiceBurnerState():
	def __init__(self, id=None, description=None):
		if id is not None:
			self.url = 'http://localhost:8000/burner_state/?id=' + str(id)
		elif description is not None:
			self.url = 'http://localhost:8000/burner_state/?description=' + str(description)
		else:
			#Invalid option
			pass

		self.request_result = requests.get(self.url)
		self.request_json = self.request_result.json()
		self.request_text = self.request_result.text

	def id(self):
		id = self.request_json[0].get('id')
		return id

	def description(self):
		description = self.request_json[0].get('description')
		return description

class WebServiceBurner():
	def __init__(self, id=None, description=None):
		if id is not None:
			self.url = 'http://localhost:8000/burner/?id=' + str(id)
		elif description is not None:
			self.url = 'http://localhost:8000/burner/?description=' + str(description)
		else:
			#Invalid option
			pass

		self.request_result = requests.get(self.url)
		self.request_json = self.request_result.json()
		self.request_text = self.request_result.text

	def id(self):
		id = self.request_json[0].get('id')
		return id

	def description(self):
		description = self.request_json[0].get('description')
		return description

	def stove_id(self):
		stove_id = self.request_json[0].get('stove')
		return stove_id

	def temperature_id(self):
		temperature_id = self.request_json[0].get('temperature')
		return temperature_id

	def temperature(self):
		web_service_temperature = WebServiceTemperature(id=self.temperature_id())
		temperature_description = web_service_temperature.description()
		return Temperature.objects.get(description=temperature_description)

	def burner_state_id(self):
		burner_state_id = self.request_json[0].get('burner_state')
		return burner_state_id

	def burner_state(self):
		web_service_burner_state = WebServiceBurnerState(id=self.burner_state_id())
		burner_state_description = web_service_burner_state.description()
		return BurnerState.objects.get(description=burner_state_description)

	def update(self, burner=None):
		if burner is None:
			burner = Burner.objects.get(description=self.description())

		web_service_temperature = WebServiceTemperature(description=burner.temperature.description)
		temperature_id = web_service_temperature.id()

		web_service_burner_state = WebServiceBurnerState(description=burner.burner_state.description)
		burner_state_id = web_service_burner_state.id()

		burner_json={'temperature': temperature_id, 'burner_state': burner_state_id, 'stove': self.stove_id(), 'description': self.description()}

		url = 'http://localhost:8000/burner/' + str(self.id()) + '/'
		requests.put(url, burner_json)

class RequestBurner():
	def get_requests(self, url):
		request_result = requests.get(url)
		request_json = request_result.json()
		return request_json

	def check_request(self, request):
		#TODO: Change tolerance
		tolerance = int(1e31)
		return int(time.time()) - int(request['new_time']) < tolerance

	def update(self):
		programming_instance = Programming()

		programming_list = programming_instance.get_list()

		for programming in programming_list:
			programming_details = programming.programming_details()

			web_service_burner = programming.burner()
			web_service_burner_id = web_service_burner.id()

			programmed_hour = programming_details.programmed_hour()
			new_temperature = programming_details.temperature()
			expected_duration = programming_details.expected_duration()
			new_web_service_burner_state = WebServiceBurnerState(description='Ligada')
			web_service_burner_state_id = new_web_service_burner_state.id()

			new_request_json = {'burner_id': web_service_burner_id,'new_temperature': new_temperature, 'new_burner_state': web_service_burner_state_id}
#			requests.put()

	def update_burners(self, url = 'http://localhost:8000/request_burner/'):
		requests = self.get_requests(url)

		for request in requests:
			if (self.check_request(request)):
				burner_web_service_id = request['burner_id']
				temperature_web_service_id = request['new_temperature']
				burner_state_web_service_id = request['new_burner_state']
				new_burner_time = int(request['new_time'])

				web_service_burner = WebServiceBurner(burner_web_service_id)
				burner_description = web_service_burner.description()
				burner = Burner.objects.get(description=burner_description)

				web_service_temperature = WebServiceTemperature(id=temperature_web_service_id)
				temperature_description = web_service_temperature.description()
				new_temperature = Temperature.objects.get(description=temperature_description)

				web_service_burner_state = WebServiceBurnerState(id=burner_state_web_service_id)
				burner_state_description = web_service_burner_state.description()
				new_burner_state = BurnerState.objects.get(description=burner_state_description)

				burner.temperature = new_temperature
				burner.burner_state = new_burner_state
				burner.time = new_burner_time

				burner.save()

			self.delete_request(request['id'])

	def delete_request(self, request_id):
		requests.delete('http://localhost:8000/request_burner/' + str(request_id))

def homepage(request):
	request_burner = RequestBurner()
	request_burner.update_burners()

	burners = Burner.objects.all()
	for burner in burners:
		web_service_burner = WebServiceBurner(description=burner.description)
		web_service_burner.update()

	return render(request, 'cooktopper/index.html', {'burners': burners, 'current_time': int(time.time())})

def burner(request, id):
	burner = Burner.objects.get(pk=id)

	command = request.GET.get('turn_burner')

	request_burner = RequestBurner()
	request_burner.update_burners()

	if(command == 'on' and burner.burner_state.description == 'Desligada'):
		burner_state_on = BurnerState.objects.get(description='Ligada')
		burner.burner_state = burner_state_on
		burner.time = int(time.time()) 
		burner.save()

		web_service_burner = WebServiceBurner(description=burner.description)
		web_service_burner.update()

	if(command == 'off'):
		burner_state_off = BurnerState.objects.get(description='Desligada')
		burner.burner_state = burner_state_off
		burner.save()

		web_service_burner = WebServiceBurner(description=burner.description)
		web_service_burner.update()


	new_temperature_description = request.GET.get('new_temperature')

	if(new_temperature_description is not None):
		new_temperature = Temperature.objects.get(description=new_temperature_description)
		burner.temperature = new_temperature
		burner.save()

		web_service_burner = WebServiceBurner(description=burner.description)
		web_service_burner.update()

	return render(request, 'cooktopper/burner.html', {'burner': burner, 'current_time': int(time.time())})

def program_burner(request, id):
	typed_start_time = request.GET.get('start_time')
	expected_duration = request.GET.get('duration')

	if (typed_start_time is not None and expected_duration is not None):
		current_hour, current_minutes = time.strftime("%H,%M").split(',')
		typed_hour, typed_minutes = typed_start_time.split(':') 

		current_time_in_seconds = int(current_hour) * 3600 + int(current_minutes) * 60
		typed_time_in_seconds = int(typed_hour) * 3600 + int(typed_minutes) * 60

		if (typed_time_in_seconds > current_time_in_seconds):
			start_time_in_seconds = int(time.time()) + (typed_time_in_seconds - current_time_in_seconds)	
		else:
			start_time_in_seconds = int(time.time()) + (24 * 3600 - current_time_in_seconds + typed_time_in_seconds)

		finish_time_in_seconds = start_time_in_seconds + int(expected_duration)

		print(start_time_in_seconds)
		print(finish_time_in_seconds)

	return render(request, 'cooktopper/program_burner.html')
