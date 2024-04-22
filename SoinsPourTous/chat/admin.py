from typing import __all__
from django.contrib import admin
from django.contrib.admin import register

from chat.models import  Message,Room
# Register your models here.


    
    
@register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['value','date','user','room']
    

@register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['code']
