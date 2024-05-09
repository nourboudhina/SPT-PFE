
from django.contrib import admin
from django.urls import path, include 
from .views import updateProfilePatient,pageProfileP,pageA, getPageAcceuil, getProfileAgent, getProfileDoctor, getProfilePatient, gestion_agent, delete_service, delete_specialite, delete_medecin, add_service, add_specialite, add_medecin, modify_medecin


urlpatterns = [
    path('updateProfile/<str:token>/', updateProfilePatient, name='update_profile_patient'),
    path('pageaccueil/<token>/',pageA),
    path('pageProfile/<token>/',pageProfileP),
    path('getpageacceuil/<token>/',getPageAcceuil),
    path('getProfilePatient/<token>/',getProfilePatient),
    path('getProfileDoctor/<token>/',getProfileDoctor),
    path('getProfileAgent/<token>/',getProfileAgent),
    path('gestionagent/<token>/',gestion_agent),
    path('delete_service/<token>/<id>/', delete_service, name='delete_service'),
    path('delete_specialite/<token>/<id>/', delete_specialite, name='delete_specialite'),
    path('delete_medecin/<token>/<id>/', delete_medecin, name='delete_medecin'),
    path('add_service/<token>/', add_service, name='add_service'),
    path('add_specialite/<token>/', add_specialite, name='add_specialite'),
    path('add_medecin/<token>/', add_medecin, name='add_medecin'),
    path('modify_medecin/<int:token>/', modify_medecin, name='modify_medecin'),

]
