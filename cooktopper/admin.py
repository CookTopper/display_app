from django.contrib import admin
from .models import Stove, BurnerState, Temperature, Burner, PanState, Pan, Programming, Shortcut

admin.site.register(Stove)
admin.site.register(BurnerState)
admin.site.register(Temperature)
admin.site.register(Burner)
admin.site.register(PanState)
admin.site.register(Pan)
admin.site.register(Programming)
admin.site.register(Shortcut)
