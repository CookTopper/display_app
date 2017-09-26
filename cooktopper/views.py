from django.shortcuts import render
from .models import Stove, BurnerState, Temperature, Burner, PanState, Pan, ProgrammingType, ProgrammingDetails, Programming, Shortcut

def homepage(request):
    return render(request, 'cooktopper/index.html', {})
