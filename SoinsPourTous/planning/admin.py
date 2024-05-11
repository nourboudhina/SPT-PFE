from typing import __all__
from django.contrib import admin
from django.contrib.admin import register

from .models import RendezVous, Payment, Apc
@admin.register(RendezVous)
class RendezVousAdmin(admin.ModelAdmin):
    list_display = ['date_rendez_vous', 'patient', 'medecin']

@admin.register(Apc)
class ApcAdmin(admin.ModelAdmin):
    list_display = ['date', 'patient', 'medecin']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'date']

    
    

    


