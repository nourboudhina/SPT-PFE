import uuid
from django.utils import timezone  # Assurez-vous d'importer correctement le module timezone
from django.db import models
from secure import PermissionsPolicy
from django.contrib.auth.models import AbstractUser, Group as DjangoGroup
from django.contrib.auth.hashers import make_password
from django.core.validators import MinLengthValidator


class Hopital(models.Model) : 
    id = models.CharField(max_length=1000,unique=True,primary_key=True)
    nom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=100)
    def __str__(self) : 
        return self.nom
    
class Service(models.Model) : 
    id = models.CharField(max_length=1000,unique=True,primary_key=True)
    service = models.CharField(max_length=100)
    hopitale = models.ForeignKey(Hopital, on_delete= models.CASCADE,related_name="hop")

class Grade(models.Model) : 
    id = models.CharField(max_length=1000,unique=True,primary_key=True)
    grade = models.CharField(max_length=100)
    def __str__(self) : 
        return self.grade
class Groupe(models.Model) : 
    id = models.CharField(max_length=1000,unique= True,primary_key=True)
    groupe = models.CharField(max_length=100)
    tarif = models.DecimalField(max_digits=5, decimal_places=3)
    def __str__(self) : 
        return self.groupe
class Specialite(models.Model) : 
    id = models.CharField(max_length=1000,unique= True,primary_key=True)
    specialite = models.CharField(max_length=100)
    service = models.ForeignKey(Service,on_delete= models.CASCADE,related_name="serv")

class Gouvernorat(models.Model):
    id = models.CharField(unique=True,max_length=1000000,primary_key=True)
    options = models.CharField(max_length=255, choices=[
        ('Ariana', 'Ariana'),
        ('Béja', 'Béja'),
        ('Ben Arous', 'Ben Arous'),
        ('Bizerte', 'Bizerte'),
        ('Gabès', 'Gabès'),
        ('Gafsa', 'Gafsa'),
        ('Jendouba', 'Jendouba'),
        ('Kairouan', 'Kairouan'),
        ('Kasserine', 'Kasserine'),
        ('Kébili', 'Kébili'),
        ('Le Kef', 'Le Kef'),
        ('Mahdia', 'Mahdia'),
        ('La Manouba', 'La Manouba'),
        ('Médenine', 'Médenine'),
        ('Monastir', 'Monastir'),
        ('Nabeul', 'Nabeul'),
        ('Sfax', 'Sfax'),
        ('Sidi Bouzid', 'Sidi Bouzid'),
        ('Siliana', 'Siliana'),
        ('Sousse', 'Sousse'),
        ('Tataouine', 'Tataouine'),
        ('Tozeur', 'Tozeur'),
        ('Tunis', 'Tunis'),
        ('Zaghouan', 'Zaghouan'),
    ])
class Nationalite(models.Model) : 
    id = models.CharField(unique=True,max_length=1000,primary_key=True)
    nationalite = models.CharField(max_length=40)

class Medecin(models.Model):
    id = models.CharField(max_length=50,unique=True,primary_key=True)
    email = models.EmailField(unique=True)
    groupe = models.ForeignKey(Groupe, on_delete= models.CASCADE,related_name="group")
    grade = models.ForeignKey(Grade, on_delete= models.CASCADE,related_name="grade_med")
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=5000)
    specialite = models.ForeignKey(Specialite,on_delete= models.CASCADE,related_name="spec")
    service = models.ForeignKey(Service,on_delete= models.CASCADE,related_name="servic")
    hopitale = models.ForeignKey(Hopital,on_delete= models.CASCADE,related_name="hopitale_med")
    phone = models.CharField(max_length = 10)
    fullname = models.CharField(max_length = 50)
    addresse = models.CharField(max_length=1000)
    gouvernorat = models.ForeignKey(Gouvernorat, on_delete= models.CASCADE,related_name="gouver")
    nationalite = models.ForeignKey(Nationalite, on_delete= models.CASCADE,related_name="natio")
    sexe = models.CharField(max_length=5)
    image = models.ImageField(upload_to='categories/')
    date_nais = models.DateField()

    def __str__(self) : 
        return self.username
    
class User( models.Model) : 
    id = models.CharField(unique=True,max_length=1000000,primary_key=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50)
    phone = models.CharField(unique=True,max_length = 10)
    fullname = models.CharField(max_length = 50)
    password = models.CharField(max_length = 5000)
    addresse = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add = True)
    gouvernorat = models.ForeignKey(Gouvernorat, on_delete= models.SET_NULL,related_name="gouv",null=True,blank=True )
    nationalite = models.ForeignKey(Nationalite, on_delete= models.CASCADE,related_name="nat",null=True,blank=True )
    sexe = models.CharField(max_length=5)
    image = models.ImageField(upload_to='categories/')
    date_naiss = models.DateField(null=True,blank=True )
    def __str__(self) : 
        return self.email
    def update_password(self, new_password):
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
    
class TokenForDoctor(models.Model) : 
    token = models.CharField(max_length = 5000)
    user = models.ForeignKey(Medecin, on_delete= models.CASCADE,related_name="tokens_set")
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self) : 
        return self.user.username
       

class Agent(models.Model) : 
    id_agent =  models.CharField(max_length=1000,unique=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=1000)
    phone = models.CharField(max_length = 10)
    email = models.EmailField(unique=True)
    hopitale = models.ForeignKey(Hopital,on_delete= models.CASCADE,related_name="hopitale_ag")
    fullname = models.CharField(max_length = 50)
    addresse = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add = True)
    gouvernorat = models.ForeignKey(Gouvernorat, on_delete= models.CASCADE,related_name="gouv_ag")
    nationalite = models.ForeignKey(Nationalite, on_delete= models.CASCADE,related_name="nat_ag")
    sexe = models.CharField(max_length=5)
    image = models.ImageField(upload_to='categories/')
    date_naiss = models.DateField()

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