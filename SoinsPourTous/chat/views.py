from random import randint
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404,redirect
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .models import  Message,Room
from account.models import TokenForDoctor,Medecin,Token, User
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password,check_password
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie,csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from SoinsPourTous.settings import TEMPLATES_BASE_URL
from rest_framework.decorators import permission_classes
from rest_framework.decorators import api_view, authentication_classes, permission_classes
    
    
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
                return JsonResponse({'erreurre': 'Médecin nexiste pas'}, status=200)

        else:
            return JsonResponse({'message': 'Code de salle non fourni'}, status=400)
    else:
        return JsonResponse({'message': 'Méthode non autorisée'}, status=405)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def send(request,token,username,room_code):
    token = TokenForDoctor.objects.filter(token=token , user__username=username).exists() if token else Token.objects.filter(token=token,user__username=username).exists()

    if request.method == 'POST':
        message = request.data.get('message')
        
        if message and username and room_code and token:
      
            if (User.objects.filter(username=username).exists() or Medecin.objects.filter(username=username).exists()) and Room.objects.filter(code = room_code).exists():
               
                user_type = 'patient' if User.objects.filter(username=username).exists() else 'medecin'
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
    

@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def getChatPatient(request, token):
    token_obj = Token.objects.filter(token=token).first()

    if request.method == 'POST':
        if token_obj:
            patient_obj = token_obj.user

            rooms = Room.objects.filter(patient=patient_obj)

            # Extract room codes
            room_codes = [room.code for room in rooms]

            return JsonResponse({"room_codes": room_codes})
        else:
            return JsonResponse({"error": "Token invalide"}, status=400)

    return JsonResponse({"error": "Requête POST requise"}, status=400)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def getChatMedecin(request, token):
    token_obj = TokenForDoctor.objects.filter(token=token).first()

    if request.method == 'POST':
        if token_obj:
            patient_obj = token_obj.user

            rooms = Room.objects.filter(medecin=patient_obj)

            # Extract room codes
            room_codes = [room.code for room in rooms]

            return JsonResponse({"room_codes": room_codes})
        else:
            return JsonResponse({"error": "Token invalide"}, status=400)

    return JsonResponse({"error": "Requête POST requise"}, status=400)

