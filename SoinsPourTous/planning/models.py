
from django.db import models
from account.models import User, Medecin


class RendezVous(models.Model) : 
    id = models.CharField(unique=True,max_length=1000,primary_key=True)
    date_rendez_vous = models.DateField()
    patient = models.ForeignKey(User,on_delete= models.CASCADE,related_name="pat_RDV")
    medecin = models.ForeignKey(Medecin,on_delete= models.CASCADE,related_name="med_RDV")
    
class Payment (models.Model) : 
    id = models.CharField(unique=True,max_length=1000,primary_key=True)
    patient = models.ForeignKey(User, on_delete= models.CASCADE,related_name="pay")
    date = models.DateField(auto_now_add=True)
    payé = models.CharField(max_length=50)
    
class Apc(models.Model) : 
    id = models.CharField(unique=True,max_length=1000,primary_key=True)
    date = models.DateTimeField()
    medecin = models.ForeignKey(Medecin,on_delete= models.CASCADE,related_name="medd")
    patient = models.ForeignKey(User,on_delete= models.CASCADE,related_name="patt")
    
class Planning(models.Model) : 
    medecin = models.ForeignKey(Medecin,on_delete= models.CASCADE,related_name="meddcin")
    patient = models.ForeignKey(User,on_delete= models.CASCADE,related_name="pattien")
    date = models.DateField()
    rdv = models.ForeignKey(RendezVous,on_delete= models.CASCADE,related_name="rdvv")
    apc = models.ForeignKey(Apc,on_delete= models.CASCADE,related_name="apcc")



    

    