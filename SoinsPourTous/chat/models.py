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
    date = models.DateTimeField(default=datetime.now , blank = True)
    user = models.CharField(max_length=1000000)
    room = models.CharField(max_length=1000000)

    



