from typing import __all__
from django.contrib import admin
from django.contrib.admin import register

from .models import Hopital, Service, Grade, Groupe, Specialite, Medecin, Gouvernorat, Nationalite, User, Otp, Token, TokenForDoctor, PasswordResetToken, Agent, TokenForAgent




@admin.register(Hopital)
class HopitalAdmin(admin.ModelAdmin):
    list_display = ['id', 'nom', 'adresse']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'service', 'hopitale']

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['id', 'grade']

@admin.register(Groupe)
class GroupeAdmin(admin.ModelAdmin):
    list_display = ['id', 'groupe', 'tarif']

@admin.register(Specialite)
class SpecialiteAdmin(admin.ModelAdmin):
    list_display = ['id', 'specialite', 'service']

@admin.register(Medecin)
class MedecinAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'password', 'groupe', 'grade', 'specialite', 'service', 'hopitale', 'email', 'phone', 'fullname', 'addresse', 'gouvernorat', 'nationalite', 'sexe', 'image', 'date_nais']

@admin.register(Gouvernorat)
class GouvernoratAdmin(admin.ModelAdmin):
    list_display = ['id', 'options']

@admin.register(Nationalite)
class NationalityAdmin(admin.ModelAdmin):
    list_display = ['id', 'nationalite']

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'password', 'username', 'phone', 'fullname', 'addresse', 'created_at', 'gouvernorat', 'nationalite', 'sexe', 'image', 'date_naiss']

@admin.register(Otp)
class OtpAdmin(admin.ModelAdmin):
    list_display = ['phone', 'otp', 'validity', 'verified']

@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ['token', 'user', 'created_at']

@admin.register(TokenForDoctor)
class TokenForDoctorAdmin(admin.ModelAdmin):
    list_display = ['token', 'user', 'created_at']

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ['id_agent', 'username', 'password', 'hopitale', 'email', 'phone', 'fullname', 'addresse', 'gouvernorat', 'nationalite', 'sexe', 'image', 'date_naiss']

@admin.register(TokenForAgent)
class TokenForAgentAdmin(admin.ModelAdmin):
    list_display = ['token', 'user', 'created_at']


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ['token', 'user', 'validity', 'created_at']