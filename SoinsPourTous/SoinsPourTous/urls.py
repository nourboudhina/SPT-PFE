
from django.contrib import admin
from django.urls import path, include 
from account.views import create_account, login, password_reset_confirm, password_reset_form, password_updated, request_otp, resend_otp, userData, verify_otp,password_reset_email, login_pour_medecin, login_pour_agent
from chat.views import checkview, send, getmessage
from accueil.views import getPageAcceuil, getProfileAgent, getProfileDoctor, getProfilePatient
from django.conf.urls.static import static

urlpatterns = [
     path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
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
    path('medecinlogin/',login_pour_medecin),
    path('agentlogin/',login_pour_agent),
    path('<token>/<username>/checkview/', checkview, name='checkview'),
    path('<token>/<username>/<room_code>/send/', send, name='send'),
    path('<token>/getMessage/<str:room>/', getmessage),
    path('getpageacceuil/<str:token>/',getPageAcceuil),
    path('getProfilePatient/<token>/',getProfilePatient),
    path('getProfileDoctor/<token>/',getProfileDoctor),
    path('getProfileAgent/<token>/',getProfileAgent),
    path("__reload__/", include("django_browser_reload.urls")),
]
