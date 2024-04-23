import uuid
from django.utils import timezone  # Assurez-vous d'importer correctement le module timezone
from django.db import models
from django.contrib.auth.models import AbstractUser, Group as DjangoGroup
from django.contrib.auth.hashers import make_password
from django.core.validators import MinLengthValidator


class Medecin(models.Model):
    username = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=5000)


class User( models.Model) : 
    email = models.EmailField(unique=True)

    username = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    phone = models.CharField(max_length = 10)
    fullname = models.CharField(max_length = 50)
    password = models.CharField(max_length = 5000)
    created_at = models.DateTimeField(auto_now_add = True)
    image = models.ImageField(upload_to='categories/')

    def __str__(self) : 
        return self.email
    def update_password(self, new_password):
        # Hasher le nouveau mot de passe avant la mise à jour
        hashed_password = make_password(new_password)
        User.objects.filter(pk=self.pk).update(password=hashed_password)
        
class Otp(models.Model) : 
    phone = models.CharField(max_length = 10)
    otp = models.IntegerField()
    validity = models.DateField(auto_now_add = True)
    verified = models.BooleanField(default = False)

    def __str__ (self) : 
        return self.phone
    

class Token(models.Model) : 
    token = models.CharField(max_length = 5000)
    user = models.ForeignKey(User, on_delete= models.CASCADE,related_name="tokens_set")
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self) : 
        return self.user.email
    
    
class TokenForDoctor(models.Model) : 
    token = models.CharField(max_length = 5000)
    user = models.ForeignKey(Medecin, on_delete= models.CASCADE,related_name="tokens_set")
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self) : 
        return self.user.username

class Agent(models.Model) : 
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=1000)


class TokenForAgent(models.Model) : 
    token = models.CharField(max_length = 5000)
    user = models.ForeignKey(Agent, on_delete= models.CASCADE,related_name="tokens")
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self) : 
        return self.user.username
class PasswordResetToken(models.Model) : 
    token = models.CharField(max_length = 5000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_tokens')
    validity = models.DateTimeField(default=timezone.now) 
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self) : 
        return self.user.email
    
    
