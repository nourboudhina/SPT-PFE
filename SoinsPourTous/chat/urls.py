
from django.contrib import admin
from django.urls import path, include 
from chat.views import get_unread_messages,get_conversation,send_message,pass_to_room,create_Room,NotificationListView, send, getmessage, getChatPatient, getChatMedecin, ChatMed, ChatPat


urlpatterns = [
    path('get_unread_messages/<token>', get_unread_messages, name='get_unread_messages'),
    path('messages/<token>/<room_code>/', get_conversation, name='get_conversation'),
    path('send_message/<token>', send_message, name='send_message'),
    path('create_Room/<token>', create_Room, name='create_Room'),
    path('pass_to_room/<token>', pass_to_room, name='pass_to_room'),
    path('<token>/<username>/<room_code>/send/', send, name='send'),
    path('getMessage/<token>/<room>/', getmessage),
    path('getPatientRooms/<token>/',getChatPatient),
    path('getMedecinRooms/<token>/',getChatMedecin),
    path('ChatMed/<token>/',ChatMed),
    path('ChatPat/<token>/',ChatPat),
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
]
