import uuid
from django.utils import timezone  # Assurez-vous d'importer correctement le module timezone
from django.db import models
from django.contrib.auth.hashers import make_password
from django.core.validators import MinLengthValidator
from datetime import datetime


    
    
class Room (models.Model) : 
    code = models.CharField(max_length=100,unique=True)
    
class Message(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(auto_now_add=True, blank = True)
    user = models.CharField(max_length=1000000)
    room = models.ForeignKey(Room,on_delete= models.CASCADE,related_name="Room")

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.value[:50] + "..."

    @property
    def formatted_timestamp(self):
        return self.date.strftime('%Y-%m-%d %H:%M:%S %Z')


    



