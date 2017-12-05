from cooktopper.models import RequestBurner
from .web_service import WebService
from .burner import WebServiceBurner
from .temperature import WebServiceTemperature
from .burner_state import WebServiceBurnerState
import requests

class WebServiceRequestBurner():
	def __init__(self, id=None, creation_time=None, request_json=None):
		if id is not None:
			self.url = WebService.url + '/request_burner/?id=' + str(id)
		elif creation_time is not None:
			self.url = WebService.url + '/request_burner/?creation_time=' + creation_time
		elif request_json is not None:
			self.request_json = request_json
		else:
			#Invalid option
			pass

		if id is not None or creation_time is not None:
			self.request_result = requests.get(self.url)
			self.request_json = self.request_result.json()[0]
			self.request_text = self.request_result.text

	def id(self):
		id = self.request_json.get('id')
		return id

	def web_service_programming_id(self):
		programming_id = self.request_json.get('programming_id')
		return programming_id

	def programmed_time(self):
		programmed_time = self.request_json.get('programmed_time')
		return programmed_time

	def web_service_burner_id(self):
		burner_id = self.request_json.get('burner_id')
		return burner_id

	def web_service_burner(self):
		burner = WebServiceBurner(id=self.web_service_burner_id())
		return burner

	def web_service_new_temperature_id(self):
		new_temperature_id = self.request_json.get('new_temperature')
		return new_temperature_id
	
	def web_service_new_temperature(self):
		new_temperature = WebServiceTemperature(id=self.web_service_new_temperature_id())
		return new_temperature

	def web_service_new_burner_state_id(self):
		new_burner_state_id = self.request_json.get('new_burner_state')
		return new_burner_state_id

	def web_service_new_burner_state(self):
		new_burner_state = WebServiceBurnerState(id=self.web_service_new_burner_state_id())
		return new_burner_state

	def create_local(self):
		request_burner = RequestBurner(burner=self.web_service_burner().get_local(), new_temperature=self.web_service_new_temperature().get_local(),
									   new_burner_state=self.web_service_new_burner_state().get_local(), programmed_time=self.programmed_time(),
									   programming_id=self.web_service_programming_id())

		print("CRIEI O REQUEST")

		request_burner.save()
		self.delete()

	def delete(self):
		requests.delete(WebService.url + '/request_burner/' + str(self.id()))
