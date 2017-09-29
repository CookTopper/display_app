from django.shortcuts import render
from .models import Stove, BurnerState, Temperature, Burner, PanState, Pan, ProgrammingType, ProgrammingDetails, Programming, Shortcut
import requests

class RequestBurner():
	def get_requests(url):
		request_result = requests.get(url)
		request_json = request_result.json()
		return request_json

	def check_request(request):
		#Put here the logic to check if too much time has passed
		return true

	def update_burner(burner):
		requests = get_requests(url)

		for request in requests:
			if (check_request(request)):
				burner.temperature = request.temperature
				burner.burner_state = request.burner_state

	def delete_request(request_id):
		#Put here the logic to delete a RequestBurner request
		pass


def homepage(request):
	requestBurner = RequestBurner()
	temperature_url = 'http://localhost:8000/temperature/'
	request_json = RequestBurner.get_requests(temperature_url)

	burners = Burner.objects.all()

	return render(request, 'cooktopper/index.html', {'burners': burners, 'request_json': request_json})

def burner(request, id):
	burner = Burner.objects.get(pk=id)
	return render(request, 'cooktopper/burner.html', {'burner': burner})
