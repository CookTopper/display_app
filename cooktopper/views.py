from django.shortcuts import render
from .models import Stove, BurnerState, Temperature, Burner, PanState, Pan, ProgrammingType, ProgrammingDetails, Programming, Shortcut

def homepage(request):
	burners = Burner.objects.all()
	return render(request, 'cooktopper/index.html', {'burners': burners})

def burner(request, id):
	burner = Burner.objects.get(pk=id)
	return render(request, 'cooktopper/burner.html', {'burner': burner})
