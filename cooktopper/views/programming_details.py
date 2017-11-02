class WebServiceProgrammingDetails():
	def __init__(self, id=None, creation_time=None, request_json=None):
		if id is not None:
			self.url = WebService.url + '/programming_details/?id=' + str(id)
		elif creation_time is not None:
			self.url = WebService.url + '/programming_details/?creation_time=' + creation_time
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

	def programmed_time(self):
		programmed_time = self.request_json[0].get('id')
		return programmed_time

	def web_service_temperature_id(self):
		temperature_id = self.request_json[0].get('temperature')

	def web_service_temperature(self):
		temperature = WebServiceTemperature(id=self.web_service_temperature_id())
		return temperature

	def web_service_burner_state_id(self):
		burner_state_id = self.request_json[0].get('new_burner_state')
		return burner_state_id

	def web_service_burner_state(self):
		burner_state = WebServiceBurnerState(id=self.web_service_burner_state_id())
		return burner_state

	def get_local(self):
		programming_details = ProgrammingDetails.objects.filter(creation_time=self.creation_time())	

		if programing_details.exists():
			return programming_details[0]
		else:
			return None

	def update_local(self):
		programming_details = self.get_local()

		if programming_details is not None:
			programming_details.programmed_time = self.programmed_time()
			programming_details.expected_duration = self.expected_duration()
			programming_details.temperature = self.web_service_temperature.get_local()
			programming_details.burner_state = self.web_service_burner_state.get_local()
		else:
			programming_details = ProgrammingDetails(programmed_time=self.programmed_time(), expected_duration=self.expected_duration(),
													 temperature=self.web_service_temperature.get_local(), creation_time=self.creation_time(),
													 burner_state=self.web_service_burner_state.get_local())
			
		programming_details.save()
