import uuid
from django.utils import timezone  
from django.db import models
from django.contrib.auth.hashers import make_password
from django.core.validators import MinLengthValidator
from datetime import datetime
class PageAcceuil(models.Model) : 
    postwithimage = models.ImageField(upload_to='categories/')
    postwithtet = models.CharField(max_length=1000)
