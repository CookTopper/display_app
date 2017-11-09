from django.shortcuts import render, render_to_response
from  cooktopper.models import Burner, BurnerState, Temperature, Programming, RequestBurner
from .request_burner import WebServiceRequestBurner
from .web_service import WebService
from .request_burner import RequestBurner
from .burner import WebServiceBurner
from .programming import WebServiceProgramming
import time
import requests

def update_local_programmings():
	url = WebService.url + '/programming/'
	web_service_programming_burners_json = requests.get(url).json()

	print (web_service_programming_burners_json)

	for web_service_programming_burner_json in web_service_programming_burners_json:
		web_service_programming = WebServiceProgramming(request_json=web_service_programming_burner_json)
		web_service_programming.create_local()

def update_local_requests():
	url = WebService.url + '/request_burner/'
	web_service_request_burners_json = requests.get(url).json()

	print (web_service_request_burners_json)

	for web_service_request_burner_json in web_service_request_burners_json:
		web_service_request_burner = WebServiceRequestBurner(request_json=web_service_request_burner_json)
		web_service_request_burner.create_local()

def update_burners_from_requests():
	requests = RequestBurner.objects.all()

	for request in requests:
		request.update_burner()
		#request.delete()

def update_remote_burners():
	url = WebService.url + '/burner/'
	web_service_burners_json = requests.get(url).json()

	print (web_service_burners_json)

	for web_service_burner_json in web_service_burners_json:
		web_service_burner = WebServiceBurner(request_json=web_service_burner_json)
		web_service_burner.update_from_local()

def update_remote_programmings():
	url = WebService.url + '/programming/'
	web_service_programmings_json = requests.get(url).json()

	print (web_service_programmings_json)

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

	if(new_temperature_description is not None):
		new_temperature = Temperature.objects.get(description=new_temperature_description)
		burner.temperature = new_temperature
		burner.save()


	return render(request, 'cooktopper/burner.html', {'burner': burner, 'current_time': int(time.time())})

def program_burner(request, burner_id):
	typed_start_time = request.GET.get('start_time')
	expected_duration = request.GET.get('duration')

	if (typed_start_time is not None and expected_duration is not None):
		current_hour, current_minutes, current_seconds = time.strftime("%H,%M,%S").split(',')
		typed_hour, typed_minutes = typed_start_time.split(':')

		current_time_in_seconds = int(current_hour) * 3600 + int(current_minutes) * 60
		typed_time_in_seconds = int(typed_hour) * 3600 + int(typed_minutes) * 60

		if (typed_time_in_seconds > current_time_in_seconds):
			start_time_in_seconds = int(time.time()) - int(current_seconds) + (typed_time_in_seconds - current_time_in_seconds)
		else:
			start_time_in_seconds = int(time.time()) - int(current_seconds) + (24 * 3600 - current_time_in_seconds + typed_time_in_seconds)

		finish_time_in_seconds = start_time_in_seconds + int(expected_duration)

		programming = Programming(temperature=Temperature.objects.get(description='media'), burner_state=BurnerState.objects.get(description='Ligada'),
								  programmed_time=start_time_in_seconds, expected_duration=expected_duration, creation_time=int(time.time()))

		programming.save()

		programming.create_request(burner_id)

		print(start_time_in_seconds)
		print(finish_time_in_seconds)

	return render(request, 'cooktopper/program_burner.html')

def view_aux(request):
	burner = Burner.objects.get(description='1')
	return render(request, 'cooktopper/aux.html', { 'burner': burner })
