from django.contrib import admin
from django.urls import path, include 
from .views import create_account, login, password_reset_confirm, password_reset_form, password_updated, request_otp, resend_otp, services, userData, verify_otp, password_reset_email, login_pour_medecin, login_pour_agent, logout_Agent, logout_medecin, logout_patient, landing, about, contact, services, loginA, loginM, loginP, Registration, Verif


urlpatterns = [
    path('',landing.as_view(), name='landing'),
    path('about/',about, name='about'),
    path('contact/',contact, name='contact'),
    path('services/',services, name='services'),
    path('Patient/',loginP, name='Patient'),
    path('Medcin/',loginM, name='Medcin'),
    path('Agent/',loginA, name='Agent'),
    path('Regis/',Registration, name='Registration'),
    path('Verification/',Verif, name='Verification'),

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
    path("logoutAgent/<token>/",logout_Agent),
    path("logoutMedecin/<token>/",logout_medecin),
    path("logoutPatient/<token>/",logout_patient),
]