from django.shortcuts import render
from .models import Stove, BurnerState, Temperature, Burner, PanState, Pan, ProgrammingType, ProgrammingDetails, Programming, Shortcut
import requests
import qrcode
import json
import time
from django.utils.crypto import get_random_string

class WebServiceStove():
	def create(self, token):
		stove_json = {'token': token}
		url = 'http://localhost:8000/stove/'
		requests.post(url, stove_json)

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
		#TODO: Change tolerance
		tolerance = int(1e31)
		return int(time.time()) - int(request['new_time']) < tolerance

	def update_burners(self, url):
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

				web_service_temperature = WebServiceTemperature(temperature_web_service_id)
				temperature_description = web_service_temperature.description()
				new_temperature = Temperature.objects.get(description=temperature_description)

				web_service_burner_state = WebServiceBurnerState(burner_state_web_service_id)
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
	while not Stove.objects.all().exists():
		stove = Stove()
		stove.token = get_random_string(length=32)

		web_service_stove = WebServiceStove()
		url = 'http://localhost:8000/stove/'
		request = requests.post(url, {'token': stove.token})

		if request.status_code == 201:
			stove.save()

	request_burner_url = 'http://localhost:8000/request_burner/'

	request_burner = RequestBurner()
	request_burner.update_burners(request_burner_url)

	burners = Burner.objects.all()

	current_time = int(time.time())

	return render(request, 'cooktopper/index.html', {'burners': burners, 'current_time': current_time})

def register(request):
	stove = Stove.objects.all()
	stove_token = stove[0].token
	qr_image = generate_qrcode(stove_token)

	return render(request, 'cooktopper/register.html')

def generate_qrcode(token):
	qr = qrcode.QRCode(
		version=1,
		box_size=10,
		border=1
	)

	qr.add_data('Paulo não usa windows')
	qr.make(fit=True)
	qr_image = qr.make_image()

	qr_image.save('cooktopper/static/image/qr_image.png')

	return qr_image

def burner(request, id):
	burner = Burner.objects.get(pk=id)
	return render(request, 'cooktopper/burner.html', {'burner': burner})
