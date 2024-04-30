
from django.contrib import admin
from django.urls import path, include 
from chat.views import checkview, send, getmessage, getChatPatient, getChatMedecin


urlpatterns = [

    path('<token>/<username>/checkview/', checkview, name='checkview'),
    path('<token>/<username>/<room_code>/send/', send, name='send'),
    path('<token>/getMessage/<str:room>/', getmessage),
    path('getPatientRooms/<token>/',getChatPatient),
    path('getMedecinRooms/<token>/',getChatMedecin),
]
