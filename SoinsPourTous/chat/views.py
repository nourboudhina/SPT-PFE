import datetime
import json
import logging
from random import randint
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404,redirect
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .models import  Message,Room
from account.models import TokenForDoctor,Medecin,Token, User
from rest_framework.parsers import FormParser
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password,check_password
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie,csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import loader
from account.serializers import   UserSerializer
from SoinsPourTous.settings import TEMPLATES_BASE_URL
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated ,DjangoModelPermissions,AllowAny
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http import Http404
from django.utils import timezone
from datetime import timedelta
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.decorators import login_required
    
    
def room(request) : 
    pass

@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def checkview(request,token,username):
    token = TokenForDoctor.objects.filter( token=token, user__username = username ).exists()
    if request.method == 'POST':
        room_code = request.data.get('room_code')
        if room_code and username and token:
            if Room.objects.filter(code=room_code).exists() and Medecin.objects.filter(username = username).exists():
                return JsonResponse({'message': 'Bienvenue dans votre chat'}, status=200)
            elif (Medecin.objects.filter(username = username).exists() and not(Room.objects.filter(code=room_code).exists())):
                new_room = Room.objects.create(code=room_code)
                new_room.save()
                return JsonResponse({'message': 'Un nouveau chat créé'}, status=200)
            else : 
                return JsonResponse({'erreurre': 'docteur nexiste pas'}, status=200)

        else:
            return JsonResponse({'message': 'Code de salle non fourni'}, status=400)
    else:
        return JsonResponse({'message': 'Méthode non autorisée'}, status=405)
    
    
from django.http import JsonResponse
from .models import Message


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def send(request,token,username,room_code):
    token = TokenForDoctor.objects.filter(token=token , user__username=username).exists() if token else Token.objects.filter(token=token,user__username=username).exists()

    if request.method == 'POST':
        message = request.data.get('message')
        
        if message and username and room_code and token:
            # Vérifier si le username appartient à un utilisateur ou à un médecin
            if (User.objects.filter(username=username).exists() or Medecin.objects.filter(username=username).exists()) and Room.objects.filter(code = room_code).exists():
                # Créez un nouvel objet Message avec les données fournies
                user_type = 'patient' if User.objects.filter(username=username).exists() else 'medecin'
                
                # Créer un nouvel objet Message avec les données fournies
                new_message = Message.objects.create(value=message, user=f'{username}-{user_type}', room=room_code)
                new_message.save()
                
                return JsonResponse({'message': 'Message envoyé avec succès'}, status=201)
            else:
                return JsonResponse({'error': 'Nom d\'utilisateur invalide'}, status=400)
        else:
            return JsonResponse({'error': 'Données manquantes'}, status=400)
    else:
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)



@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def getmessage(request, room,token):
    token = TokenForDoctor.objects.filter( token=token).exists()

    try:
        room_details = Room.objects.get(code=room)
        messages = Message.objects.filter(room=room_details.code).order_by('date')
        return JsonResponse({'messages': list(messages.values())}, status=200)
    except Room.DoesNotExist:
        return JsonResponse({'error': 'La salle spécifiée n\'existe pas'}, status=404)
