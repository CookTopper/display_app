from django.shortcuts import render, render_to_response
from  cooktopper.models import Burner, BurnerState, Temperature, Programming, RequestBurner, Stove
from .request_burner import WebServiceRequestBurner
from .web_service import WebService
from .request_burner import RequestBurner
from .burner import WebServiceBurner
from .programming import WebServiceProgramming
import time
import requests
import qrcode
from django.http import HttpResponse
import json
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt

def update_local_programmings():
	url = WebService.url + '/programming/'
	web_service_programming_burners_json = requests.get(url).json()

	for web_service_programming_burner_json in web_service_programming_burners_json:
		web_service_programming = WebServiceProgramming(request_json=web_service_programming_burner_json)
		web_service_programming.create_local()

def update_local_requests():
	url = WebService.url + '/request_burner/'
	web_service_request_burners_json = requests.get(url).json()

	for web_service_request_burner_json in web_service_request_burners_json:
		web_service_request_burner = WebServiceRequestBurner(request_json=web_service_request_burner_json)
		web_service_request_burner.create_local()

def update_burners_from_requests():
	requests = RequestBurner.objects.all()

	for request in requests:
		request.update_burner()

def update_remote_burners():
	url = WebService.url + '/burner/'
	web_service_burners_json = requests.get(url).json()

	for web_service_burner_json in web_service_burners_json:
		web_service_burner = WebServiceBurner(request_json=web_service_burner_json)
		web_service_burner.update_from_local()

def update_remote_programmings():
	url = WebService.url + '/programming/'
	web_service_programmings_json = requests.get(url).json()

	for web_service_programming_json in web_service_programmings_json:
		web_service_programming = WebServiceProgramming(request_json=web_service_programming_json)
		web_service_programming.update_from_local()

def homepage(request):
	update_local_requests()

	update_burners_from_requests()
	update_remote_burners()

	update_local_programmings()
	update_remote_programmings()

	burners = Burner.objects.all()

	return render(request, 'cooktopper/index.html', {'burners': burners, 'current_time': int(time.time())})

def scale(request):

	return render(request, 'cooktopper/scale.html')

def burner(request, id):
	burner = Burner.objects.get(pk=id)

	command = request.GET.get('turn_burner')

	if(command == 'on' and burner.burner_state.description == 'Desligada'):
		burner_state_on = BurnerState.objects.get(description='Ligada')
		burner.burner_state = burner_state_on
		burner.time = int(time.time())
		burner.save()

	if(command == 'off'):
		burner_state_off = BurnerState.objects.get(description='Desligada')
		burner.burner_state = burner_state_off
		burner.save()


	new_temperature_description = request.GET.get('new_temperature')


	print(new_temperature_description)

	if(new_temperature_description is not None):
		print(new_temperature_description)

		new_temperature = Temperature.objects.get(description=new_temperature_description)
		burner.temperature = new_temperature
		burner.save()

	return render(request, 'cooktopper/burner.html', {'burner': burner, 'current_time': int(time.time())})

def program_burner(request, burner_id):
	burner = Burner.objects.get(id=burner_id)

	new_temperature_description = request.GET.get('new_temperature')

	typed_start_time = request.GET.get('start_time')
	typed_finish_time = request.GET.get('finish_time')

	new_temperature_description='media'
	if (typed_start_time is not None and typed_finish_time is not None):
		current_hour, current_minutes, current_seconds = time.strftime("%H,%M,%S").split(',')
		typed_hour, typed_minutes = typed_start_time.split(':')
		typed_finish_hour, typed_finish_minutes = typed_finish_time.split(':')

		current_time_in_seconds = int(current_hour) * 3600 + int(current_minutes) * 60
		typed_time_in_seconds = int(typed_hour) * 3600 + int(typed_minutes) * 60
		typed_finish_time_in_seconds = int(typed_finish_hour) * 3600 + int(typed_finish_minutes) * 60

		if (typed_finish_time_in_seconds > typed_time_in_seconds):
			expected_duration = typed_finish_time_in_seconds - typed_time_in_seconds
		else:
			expected_duration = 24 * 3600 - typed_time_in_seconds * 60 + typed_finish_time_in_seconds * 60

		if (typed_time_in_seconds > current_time_in_seconds):
			start_time_in_seconds = int(time.time()) - int(current_seconds) + (typed_time_in_seconds - current_time_in_seconds)
		else:
			start_time_in_seconds = int(time.time()) - int(current_seconds) + (24 * 3600 - current_time_in_seconds + typed_time_in_seconds)

		finish_time_in_seconds = start_time_in_seconds + int(expected_duration)

		new_temperature = Temperature.objects.get(description=new_temperature_description)

		programming = Programming(temperature=new_temperature, burner_state=BurnerState.objects.get(description='Ligada'),
								  programmed_time=start_time_in_seconds, expected_duration=expected_duration, creation_time=int(time.time()))

		programming.save()

		programming.create_request(burner_id)

		print(start_time_in_seconds)
		print(finish_time_in_seconds)

	return render(request, 'cooktopper/program_burner.html', {'burner': burner, 'current_time': int(time.time())})

def register(request):
	stove = Stove.objects.all()
	stove_token = stove[0].token

	print(stove[0].token)

	print("StoveToken: " + stove_token)

	qr_image = generate_qrcode(stove_token)

	return render(request, 'cooktopper/register.html')

def choose_burner(request):
	burners = Burner.objects.all()

	return render(request, 'cooktopper/choose_burner.html', {'burners': burners})

@csrf_exempt
def server_burner(request):
	if (request.method == "POST"):
		print("POST")

		if (request.POST.get('burner_state') is not None):
			print(request.POST.get('burner_state'))

		if (request.POST.get('temperature') is not None):
			print(request.POST.get('temperature'))

	elif (request.method == "GET"):
		print("GET")

	burner = Burner.objects.all()

	burner_json = json.dumps([{'burner': 1, 'burner_state': burner[0].burner_state.description, 'temperature': burner[0].temperature.description}, {'burner': 2, 'burner_state': burner[1].burner_state.description, 'temperature': burner[1].temperature.description}])

	return HttpResponse(burner_json, content_type='application/json')

def generate_qrcode(token):
	qr = qrcode.QRCode(
		version=1,
		box_size=10,
		border=1
	)

	print("TOKEN: " + token)

	qr.add_data(token)
	qr.make(fit=True)
	qr_image = qr.make_image()

	qr_image.save('cooktopper/static/image/qr_image.png')

	return qr_image
