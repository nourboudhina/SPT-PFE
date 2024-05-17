
from django.contrib import admin
from django.urls import path, include 
from chat.views import NotificationListView, checkview, checkRoom, send, getmessage, getChatPatient, getChatMedecin, ChatMed, ChatPat


urlpatterns = [

    path('<token>/<username>/checkview/', checkview, name='checkview'),
    path('<token>/<username>/checkRoom/', checkRoom, name='checkRoom'),
    path('<token>/<username>/<room_code>/send/', send, name='send'),
    path('<token>/getMessage/<str:room>/', getmessage),
    path('getPatientRooms/<token>/',getChatPatient),
    path('getMedecinRooms/<token>/',getChatMedecin),
    path('ChatMed/<token>/',ChatMed),
    path('ChatPat/<token>/',ChatPat),
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
]
