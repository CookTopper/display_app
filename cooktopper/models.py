from django.db import models
import time

class Stove(models.Model):
	token = models.CharField(blank=False, max_length=45)

class BurnerState(models.Model):
	description = models.CharField(blank=False, max_length=45)

class Temperature(models.Model):
	description = models.CharField(blank=False, max_length=45)

class Burner(models.Model):
	description = models.CharField(blank=False, max_length=45)
	stove = models.ForeignKey(Stove, on_delete=models.CASCADE)
	temperature = models.ForeignKey(Temperature, on_delete=models.CASCADE)
	burner_state = models.ForeignKey(BurnerState, on_delete=models.CASCADE)
	time = models.IntegerField()

	def update(self, temperature, burner_state, time):
		if (burner_state != self.burner_state):
			self.time = time

		self.temperature = temperature
		self.burner_state = burner_state

class RequestBurner(models.Model):
	burner = models.ForeignKey(Burner, on_delete=models.CASCADE)
	new_temperature = models.ForeignKey(Temperature, on_delete=models.CASCADE)
	new_burner_state = models.ForeignKey(BurnerState, on_delete=models.CASCADE)
	programmed_time = models.IntegerField()
	programming_id = models.IntegerField()

	def check_request(self):
		print("programmed time: ", self.programmed_time)
		print("time: ", time.time())
		return (int(time.time()) - self.programmed_time) >=0 and (int(time.time()) - self.programmed_time) < 10 

	def update_burner(self):
		check_request = self.check_request()
		print("entrei no update burner")
		if (check_request):
			print("passei no check")
			print("Temperatura: ", self.new_temperature.description)
			print("Burner State: ", self.new_burner_state.description)
			print("Time: ", self.programmed_time)
			self.burner.update(temperature=self.new_temperature, burner_state=self.new_burner_state, time=self.programmed_time)			
			self.burner.save()
			self.delete()

		return check_request

class PanState(models.Model):
	description = models.CharField(blank=False, max_length=45)

class Pan(models.Model):
	code = models.CharField(blank=False, max_length=45)
	temperature = models.IntegerField()
	pan_state = models.ForeignKey(PanState, on_delete=models.CASCADE)

class Programming(models.Model):
	temperature = models.ForeignKey(Temperature, on_delete=models.CASCADE)
	burner_state = models.ForeignKey(BurnerState, on_delete=models.CASCADE)
	programmed_time = models.IntegerField()
	expected_duration = models.IntegerField()
	creation_time = models.IntegerField()

	def check_request(self):
		request = RequestBurner.objects.filter(programming_id=self.id)

		return (request.exists() == False)

	def create_request(self, burner_id):
		print("entrei\n\n\n\n\n\n\n")
		if (self.check_request()):
			print("entrei2\n\n\n\n\n\n\n")
			request_start = RequestBurner(burner=Burner.objects.get(id=burner_id), new_burner_state=self.burner_state,
										  new_temperature=self.temperature, programmed_time=self.programmed_time,
										  programming_id=self.id)

			if (self.expected_duration != -1):
				request_finish = RequestBurner(burner=Burner.objects.get(id=burner_id), new_burner_state=BurnerState.objects.get(description='Desligada'),
											   new_temperature=self.temperature, programmed_time=int(self.programmed_time) + int(self.expected_duration),
											   programming_id=self.id)

			request_start.save()

			if (self.expected_duration != -1):
				request_finish.save()

class Shortcut(models.Model):
	description = models.CharField(blank=False, max_length=45)
	programming = models.ForeignKey(Programming, on_delete=models.CASCADE)
