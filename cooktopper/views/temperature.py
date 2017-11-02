from cooktopper.models import Temperature
from .web_service import WebService
import requests

class WebServiceTemperature():
	def __init__(self, id=None, description=None, request_json=None):
		if id is not None:
			self.url = WebService.url + '/temperature/?id=' + str(id)
		elif description is not None:
			self.url = WebService.url + '/temperature/?description=' + str(description)
		elif request_json is not None:
			self.request_json = request_json
		else:
			#Invalid Option
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

	def get_local(self):
		temperature = Temperature.objects.filter(description=self.description())

		if temperature.exists():
			return temperature[0]
		else:
			return None
