from typing import __all__
from django.contrib import admin
from django.contrib.admin import register

from account.models import  Agent, Medecin, Otp, PasswordResetToken,  Token, TokenForAgent, TokenForDoctor, User
# Register your models here.



@register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email','phone','fullname','created_at']


    
@register(Medecin)
class MedecinAdmin(admin.ModelAdmin) : 
    list_display = ['id','username']

@register(Otp)
class OtpAdmin(admin.ModelAdmin) : 
    list_display = ['phone', 'otp','validity','verified']

@register(Token)
class TokenAdmin(admin.ModelAdmin) : 
    list_display = ['token','user','created_at']
    
    
@register(TokenForDoctor)
class TokenDoctor(admin.ModelAdmin) : 
    list_display = ['token','user','created_at']


@register(TokenForAgent)
class TokenAgent(admin.ModelAdmin) : 
    list_display = ['token','user','created_at']


@register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin) : 
    list_display=['token','user','created_at']
    

@register(Agent)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['username','password']




