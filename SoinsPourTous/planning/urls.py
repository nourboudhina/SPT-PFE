
from django.contrib import admin
from django.urls import path, include 
from .views import ajout_rendez_vous_par_agent, envoyer_rappel_rendez_vous, ajout_APC_par_agent, get_Planning_Doctor, get_PaiementHistorique, suivi_apc, get_agent_rendezvous_apc,get_RendezVousH_Patient, get_APCH_Patient, get_Planning_Patient, get_RendezVousH_Doctor, get_APCH_Doctor, update_D, update_RendezVous_Date_A, update_APC_Date_A, delete_D, delete_RendezVous_A, delete_APC_A, getApcForAgent, delete_payment, add_payment, update_payment 

urlpatterns = [
    path('ajoutRendezVousParAgent/<token>/',ajout_rendez_vous_par_agent),
    path('ajoutAPCParAgent/<token>/',ajout_APC_par_agent),
    path('envoyer_rappel_rendez_vous/', envoyer_rappel_rendez_vous, name='envoyer_rappel_rendez_vous'),
    path('getpaiementHistorique/<token>/',get_PaiementHistorique),
    path('get_Planning_Doctor/<token>/',get_Planning_Doctor),
    path('suivi_apc/<token>/',suivi_apc),
    path('get_agent_rendezvous_apc/<int:token>/',get_agent_rendezvous_apc, name='get_agent_rendezvous_apc'),
    path('getPatientRdvH/<token>/',get_RendezVousH_Patient),
    path('get_APCH_Patient/<token>/',get_APCH_Patient),
    path("getPatientRdv/<token>/",get_Planning_Patient),
    path("getRdvHDoctor/<token>/",get_RendezVousH_Doctor),
    path('get_APCH_Doctor/<token>/',get_APCH_Doctor),
    path("updateDateDoctor/<token>/<type>/<id>/",update_D),
    path("updateRdvDateAgent/<token>/<rendez_vous_id>/",update_RendezVous_Date_A),
    path('update_APC_Date_A/<token>/<apc_id>',update_APC_Date_A),
    path("deleteRendezVousDoctor/<token>/<type>/<id>/",delete_D),
    path("deleteRendezVousAgent/<token>/<rendez_vous_id>/",delete_RendezVous_A),
    path('delete_APC_A/<token>/<apc_id>',delete_APC_A),
    path("getApcForAgent/<token>/",getApcForAgent),
    path("delete_payment/<token>/<payment_id>/",delete_payment),
    path("add_payment/<token>/",add_payment),
    path("update_payment/<token>/<payment_id>/",update_payment),
    
   
]
