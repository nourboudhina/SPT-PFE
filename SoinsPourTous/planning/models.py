
from django.db import models
   
class RendezVous(models.Model) : 
    date_rendez_vous = models.DateField()
    patient = models.CharField(max_length =  100)
    medecin = models.CharField(max_length =  100)


    

    