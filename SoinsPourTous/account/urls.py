from django.contrib import admin
from django.urls import path, include 
from .views import edit_specialite,edit_service,list_patient,get_gouvernorats,list_nationalites,add_medecin,delete_medecin,list_medecins,list_grades, list_groupes,delete_specialite,add_specialiter,add_service, delete_service, list_services,create_account, login, password_reset_confirm, password_reset_form, password_updated, request_otp, resend_otp, userData, verify_otp, password_reset_email, login_pour_medecin, login_pour_agent, logout_Agent, logout_medecin, logout_patient, landing, about, contact, loginA, loginM, loginP, Registration, Verif, Personnel
from . import views

urlpatterns = [
    path('patients/', list_patient, name='list_patient'),
    path('medecins/', list_medecins, name='list-medecins'),
    path('medecins/add/', add_medecin, name='add_medecin'),
    path('medecins/delete/<str:pk>/', delete_medecin, name='delete-medecin'),
    path('grades/', list_grades, name='list-grades'),
    path('groupes/', list_groupes, name='list-groupes'),
    path('nationalites/', list_nationalites, name='list-nationalites'),
    path('specialites/', views.specialite_list, name='specialite_list'),
    path('specialites/add/', add_specialiter, name='specialite_detail'),
    path('services/', list_services, name='list_services'),
    path('services/edit/', edit_service, name='edit_service'),
    path('services/add/', add_service, name='add_service'),
    path('specialites/edit/', edit_specialite, name='edit_specialite'),
    path('specialites/delete/<str:pk>/', delete_specialite, name='delete_specialite'),
    path('services/delete/<str:pk>/', delete_service, name='delete_service'),
    path('',landing.as_view(), name='landing'),
    path('Personnel/',Personnel, name='Personnel'),
    path('about/',about, name='about'),
    path('contact/',contact, name='contact'),
    path('Patient/',loginP, name='Patient'),
    path('Medcin/',loginM, name='Medcin'),
    path('Agent/',loginA, name='Agent'),
    path('Regis/',Registration, name='Registration'),
    path('Verification/',Verif, name='Verification'),
    path('gouvernorats/', get_gouvernorats, name='gouvernorats-api'),
    path('request_otp/',request_otp, name = 'request_otp'),
    path('resend_otp/',resend_otp,name='resend_otp'),
    path('verify_otp/', verify_otp),
    path('create_account/',create_account, name = 'create_account'),
    path('password_reset_email/',password_reset_email,name='password_reset_email'),
    path('password_reset_form/<email>/<token>/', password_reset_form, name='password_reset_form'),
    path('login/',login,name='login'),
    path('password_reset_confirm/<email>/<token>',password_reset_confirm,name='password_reset_confirm'),
    path('password_updated/', password_updated, name='password_updated'),
    path('userdata/',userData,name='userdata'),
    path('medecinlogin/',login_pour_medecin,name='medecinlogin'),
    path('agentlogin/',login_pour_agent, name='agentlogin'),
    path("logoutAgent/<str:token>/",logout_Agent),
    path("logoutMedecin/<str:token>/",logout_medecin),
    path("logoutPatient/<str:token>/",logout_patient),
]