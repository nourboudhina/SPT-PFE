from random import randint
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from account.models import TokenForDoctor,Token, TokenForAgent
from rest_framework.decorators import api_view
from rest_framework.decorators import api_view, authentication_classes
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .models import PageAcceuil

import base64

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def getPageAcceuil(request, token):
    token_obj = TokenForDoctor.objects.filter(token=token).exists() if token else Token.objects.filter(token=token).exists()
    if request.method == 'GET':
        if token_obj:
            page_acceuil_data = PageAcceuil.objects.values()  # Obtenir toutes les données
            for data in page_acceuil_data:
                postwithimage_path = data['postwithimage']
                with open(postwithimage_path, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                data['postwithimage'] = encoded_string  # Remplacer le chemin d'accès par la représentation base64
            return JsonResponse(list(page_acceuil_data), safe=False)  # Renvoyer les données au format JSON
        else:
            return JsonResponse({"error": "Token invalide"}, status=400)
        
        
        
from django.http import JsonResponse
import base64

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def getProfilePatient(request, token):
    token_obj = Token.objects.filter(token=token).first()
    if request.method == 'GET':
        if token_obj:
            user_obj = token_obj.user
            username_patient = user_obj.username
            email_patient = user_obj.email
            phone_patient = user_obj.phone
            fullname_patient = user_obj.fullname
            image_path = user_obj.image.path
            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            user_data = {
                'username': username_patient,
                'email': email_patient,
                'phone': phone_patient,
                'fullname': fullname_patient,
                'image': encoded_string
            }

            # Retour des données sous forme de réponse JSON
            return JsonResponse(user_data)
        else:
            return JsonResponse({"error": "Token invalide"}, status=400)
        
        
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def getProfileDoctor(request, token):
    token_obj = TokenForDoctor.objects.filter(token=token).first()
    if request.method == 'GET':
        if token_obj:
            user_obj = token_obj.user
       
            username_patient = user_obj.username

            
            user_data = {
                'username': username_patient,
            }

            # Retour des données sous forme de réponse JSON
            return JsonResponse(user_data)
        else:
            return JsonResponse({"error": "Token invalide"}, status=400)
        
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def getProfileAgent(request, token):
    token_obj = TokenForAgent.objects.filter(token=token).first()
    if request.method == 'GET':
        if token_obj:
            user_obj = token_obj.user
       
            username_agent = user_obj.username

            
            user_data = {
                'username': username_agent,
            }

            
            return JsonResponse(user_data)
        else:
            return JsonResponse({"error": "Token invalide"}, status=400)