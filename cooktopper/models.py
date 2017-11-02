from django.db import models

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
		self.temperature = temperature
		self.burner_state = burner_state
		self.time = time

class RequestBurner(models.Model):
	burner = models.ForeignKey(Burner, on_delete=models.CASCADE)
	new_temperature = models.ForeignKey(Temperature, on_delete=models.CASCADE)
	new_burner_state = models.ForeignKey(BurnerState, on_delete=models.CASCADE)
	programmed_time = models.IntegerField()
	programming_id = models.IntegerField()

	def check_request(self):
		return True

	def update_burner(self):
		check_request = self.check_request()
		if (check_request):
			self.burner.update(temperature=self.new_temperature, burner_state=self.new_burner_state, time=self.programmed_time)			
			self.burner.save()

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

class Shortcut(models.Model):
	description = models.CharField(blank=False, max_length=45)
	programming = models.ForeignKey(Programming, on_delete=models.CASCADE)
