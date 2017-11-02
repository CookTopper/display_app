class WebServiceProgramming():
	def __init__(self, id=None, creation_time=None, request_json=None):
		if id is not None:
			self.url = WebService.url + '/programming/?id=' + str(id)
		elif description is not None:
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
		id = self.request_json[0].get('id')
		return id

	def creation_time(self):
		creation_time = self.request_json[0].get('creation_time')
		return creation_time

	def web_service_burner_id(self):
		burner_id = self.request_json[0].get('burner')
		return burner_id 

	def web_service_burner(self):
		burner = WebServiceBurner(id=self.web_service_burner_id())
		return burner 

	def web_service_programming_details_id(self):
		programming_details_id = self.request_json[0].get('programming_details')
		return programming_details

	def web_service_programming_details(self):
		programming_details = WebServiceProgrammingDetails(id=self.web_service_programming_details_id())
		return programming_details 

	def update_from_local(self):
		programming = self.get_local()
		programming_json = {'temperature': WebServiceTemperature(description=programming.temperature.description).id(),
							'burner_state': WebServiceBurnerState(description=programming.burner_state.description).id(),
							'programmed_time': programming.programmed_time, 'expected_duration': programming.expected_duration,
							'creation_time': programming.creation_time}

		requests.put(WebService.url + '/programming/' + str(self.id()) + '/', programming_json)

	def get_local(self):
		programming = Programming.objects.filter(creation_time=self.creation_time())

		if programing.exists():
			return programming[0]
		else:
			return None

	def create_local(self):
		programming = self.get_local()

		if programming is None:
			programming = Programming(creation_time=self.creation_time(), burner=self.web_service_burner.get_local(),
									  programming_details=self.web_service_programming_details.get_local())
			programming.save()
