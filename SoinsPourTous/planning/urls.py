
from django.contrib import admin
from django.urls import path, include 
from .views import ajout_rendez_vous_par_agent, envoyer_rappel_rendez_vous, getPaiementHistorique, suivi_apc, get_agent_rendezvous_apc,getRendezVousHPatient, getRendezVousPatient, getRendezVousHDoctor, updateRendezVousDateD, updateRendezVousDateA, deleteRendezVousD, deleteRendezVousA, getApcForAgent, delete_payment, add_payment, update_payment

urlpatterns = [
    path('ajoutRendezVousParAgent/<token>/',ajout_rendez_vous_par_agent),
    path('envoyer_rappel_rendez_vous/', envoyer_rappel_rendez_vous, name='envoyer_rappel_rendez_vous'),
    path('getpaiementHistorique/<token>/',getPaiementHistorique),
    path('suivi_apc/<token>/',suivi_apc),
    path('get_agent_rendezvous_apc/<int:token>/',get_agent_rendezvous_apc, name='get_agent_rendezvous_apc'),
    path('getPatientRdvH/<token>/',getRendezVousHPatient),
    path("getPatientRdv/<token>/",getRendezVousPatient),
    path("getRdvHDoctor/<token>/",getRendezVousHDoctor),
    path("updateRdvDateDoctor/<token>/<rendez_vous_id>/",updateRendezVousDateD),
    path("updateRdvDateAgent/<token>/<rendez_vous_id>/",updateRendezVousDateA),
    path("deleteRendezVousDoctor/<token>/<rendez_vous_id>/",deleteRendezVousD),
    path("deleteRendezVousAgent/<token>/<rendez_vous_id>/",deleteRendezVousA),
    path("getApcForAgent/<token>/",getApcForAgent),
    path("delete_payment/<token>/<payment_id>/",delete_payment),
    path("add_payment/<token>/",add_payment),
    path("update_payment/<token>/<payment_id>/",update_payment),
    
   
]
