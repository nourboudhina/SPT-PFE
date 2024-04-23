from typing import __all__
from django.contrib import admin
from django.contrib.admin import register

from .models import RendezVous
@register(RendezVous)
class RAdmin(admin.ModelAdmin):
    list_display = ['date_rendez_vous','medecin','patient']

    
    

    


