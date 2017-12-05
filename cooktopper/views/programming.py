from  cooktopper.models import Programming
from .burner import WebServiceBurner
from .temperature import WebServiceTemperature
from .burner_state import WebServiceBurnerState
from .web_service import WebService

import requests

class WebServiceProgramming():
	def __init__(self, id=None, creation_time=None, request_json=None):
		if id is not None:
			self.url = WebService.url + '/programming/?id=' + str(id)
		elif creation_time is not None:
			self.url = WebService.url + '/programming/?creation_time=' + creation_time
		elif request_json is not None:
			self.request_json = request_json
		else:
			#Invalid option
			pass

		if id is not None or creation_time is not None:
			self.request_result = requests.get(self.url)
			self.request_json = self.request_result.json()
			self.request_text = self.request_result.text

	def id(self):
		id = self.request_json.get('id')
		return id

	def creation_time(self):
		creation_time = self.request_json.get('creation_time')
		return creation_time

	def expected_duration(self):
		expected_duration = self.request_json.get('expected_duration')
		return expected_duration

	def programmed_time(self):
		programmed_time = self.request_json.get('programmed_time')
		return programmed_time

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

	def get_local(self):
		programming = Programming.objects.filter(creation_time=self.creation_time())

		if programming.exists():
			return programming[0]
		else:
			return None

	def update_from_local(self):
		programming = self.get_local()
		programming_json = {'temperature': WebServiceTemperature(description=programming.temperature.description).id(),
							'burner_state': WebServiceBurnerState(description=programming.burner_state.description).id(),
							'programmed_time': programming.programmed_time, 'expected_duration': programming.expected_duration,
							'creation_time': programming.creation_time}

		requests.put(WebService.url + '/programming/' + str(self.id()) + '/', programming_json)


	def create_local(self):
		programming = self.get_local()

		if programming is None:
			programming = Programming(creation_time=self.creation_time(), expected_duration=self.expected_duration(),
									  programmed_time=self.programmed_time(), temperature=self.web_service_temperature().get_local(),
									  burner_state=self.web_service_burner_state().get_local())

			programming.save()
