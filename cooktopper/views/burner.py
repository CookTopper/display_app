import requests
from cooktopper.models import Burner
from cooktopper.models import Temperature
from cooktopper.models import BurnerState
from .web_service import WebService
from .temperature import WebServiceTemperature
from .burner_state import WebServiceBurnerState

class WebServiceBurner():
	def __init__(self, id=None, description=None, request_json=None):
		if id is not None:
			self.url = WebService.url + '/burner/?id=' + str(id)
		elif description is not None:
			self.url = WebService.url + '/burner/?description=' + str(description)
		elif request_json is not None:
			self.request_json = request_json
		else:
			#Invalid option
			pass

		if id is not None or description is not None:
			self.request_result = requests.get(self.url)
			self.request_json = self.request_result.json()[0]
			self.request_text = self.request_result.text

	def id(self):
		id = self.request_json.get('id')
		return id

	def description(self):
		description = self.request_json.get('description')
		return description

	def web_service_stove_id(self):
		stove_id = self.request_json.get('stove')
		return stove_id

	def web_service_stove(self):
		stove = WebServiceStove(id=self.web_service_stove_id())
		return stove

	def web_service_temperature_id(self):
		temperature_id = self.request_json.get('temperature')
		return temperature_id

	def web_service_temperature(self):
		temperature = WebServiceTemperature(id=self.web_service_temperature_id())
		return temperature

	def web_service_burner_state_id(self):
		burner_state_id = self.request_json.get('burner_state')
		return burner_state_id

	def web_service_burner_state(self):	
		burner_state = WebServiceBurnerState(id=self.web_service_burner_state_id())
		return burner_state

	def update_from_local(self):
		burner = self.get_local()
		burner_json = {'description': self.description(), 'stove': self.web_service_stove_id(),
					   'temperature': WebServiceTemperature(description=burner.temperature.description).id(),
					   'burner_state': WebServiceBurnerState(description=burner.burner_state.description).id(),
					   'time': burner.time}
		requests.put(WebService.url + '/burner/' + str(self.id()) + '/', burner_json)

	def get_local(self):
		burner = Burner.objects.filter(description=self.description())

		if burner.exists():
			return burner[0]
		else:
			return None
