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

class PanState(models.Model):
	description = models.CharField(blank=False, max_length=45)

class Pan(models.Model):
	code = models.CharField(blank=False, max_length=45)
	temperature = models.IntegerField()
	pan_state = models.ForeignKey(PanState, on_delete=models.CASCADE)

class ProgrammingType(models.Model):
	description = models.CharField(blank=False, max_length=45)

class ProgrammingDetails(models.Model):
	programmed_hour = models.CharField(blank=False, max_length=45)
	expected_duration = models.IntegerField()
	programming_type = models.ForeignKey(ProgrammingType, on_delete=models.CASCADE)
	temperature = models.ForeignKey(Temperature, on_delete=models.CASCADE)

class Programming(models.Model):
	burner = models.ForeignKey(Burner, on_delete=models.CASCADE)
	programming_details = models.ForeignKey(ProgrammingDetails, on_delete=models.CASCADE)

class Shortcut(models.Model):
	description = models.CharField(blank=False, max_length=45)
	programming_details = models.ForeignKey(ProgrammingDetails, on_delete=models.CASCADE)
