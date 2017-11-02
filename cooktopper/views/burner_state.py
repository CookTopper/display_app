from cooktopper.models import BurnerState 
from .web_service import WebService
import requests

class WebServiceBurnerState():
	def __init__(self, id=None, description=None, request_json=None):
		if id is not None:
			self.url = WebService.url + '/burner_state/?id=' + str(id)
		elif description is not None:
			self.url = WebService.url + '/burner_state/?description=' + str(description)
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

	def get_local(self):
		burner_state = BurnerState.objects.filter(description=self.description())

		if burner_state.exists():
			return burner_state[0]
		else:
			# This should not happen
			return None
