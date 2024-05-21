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
from rest_framework.response import Response

@csrf_exempt
def ChatMed(request, token):
    token = TokenForDoctor.objects.filter(token=token).first()
    return render(request, 'Chat/ListChatMédecin.html') 
@csrf_exempt
def ChatPat(request, token):
    token = Token.objects.filter(token=token).first()
    return render(request, 'Chat/ListChatPatient.html') 
def room(request) : 
    pass
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def create_Room(request,token):
    token_obj = TokenForDoctor.objects.filter(token=token).first()
    if token_obj:
        user_obj = token_obj.user
        if request.method == 'POST':
            room_code = request.data.get('room_code')
            id=request.data.get('patientId')
            patientobj=User.objects.filter(id=id).first()
            print(room_code)
            if Room.objects.filter(medecin=user_obj,patient=patientobj).exists():
                return JsonResponse({'message': 'Bienvenue dans votre chat'}, status=200)
            else : 
                room = Room.objects.create(code=room_code, medecin=user_obj,patient=patientobj)
                room.save()
                return JsonResponse({'message': 'room created '}, status=200)
        else:
            return JsonResponse({'message': 'Méthode non autorisée'}, status=405)
    
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def pass_to_room(request,token):
    token_obj = Token.objects.filter(token=token).first()
    if request.method == 'POST':
        if token_obj:
            user_obj = token_obj.user
            room_code = request.data.get('room_code')
            id=request.data.get('medId')
            medobj=Medecin.objects.filter(id=id).first()
            if Room.objects.filter(code=room_code).exists():
                if Room.objects.filter(code=room_code,patient=user_obj,medecin=medobj).exists():
                    return JsonResponse({'message': 'Bienvenue dans votre chat'}, status=200)
                else:

                    return JsonResponse({'message': 'non autorisée'}, status=200)
            else : 
                return JsonResponse({'erreurre': 'room not exist '}, status=200)

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


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def send_message(request, token):
    # Determine if the token belongs to a doctor or a patient
    doctor = TokenForDoctor.objects.filter(token=token).first()
    patient = None if doctor else Token.objects.get(token=token)

    if not (doctor or patient):
        return JsonResponse({"error": "Token invalide ou expiré"}, status=400)

    # Extract the sender object based on the token type
    sender = doctor.user if doctor else patient.user

    # Extract data from POST request
    room_code = request.data.get('room_code')
    message_value = request.data.get('message')
    receiver_id = request.data.get('receiver_id')  # ID of the receiver from request

    if not all([room_code, message_value, receiver_id]):
        return JsonResponse({"error": "Paramètres manquants"}, status=400)

    try:
        # Retrieve the room by the provided room_code
        room = Room.objects.get(code=room_code)

        # Create a new message with sender and receiver
        new_message = Message.objects.create(
            value=message_value,
            sender=sender.id,  # Assuming 'user' is a username field
            receiver=receiver_id,  # Assuming receiver_id is directly usable
            room=room,
        )

        return JsonResponse({
            "message": new_message.value,
            "message_id": new_message.id,
            "timestamp": new_message.formatted_timestamp
        }, status=201)

    except Room.DoesNotExist:
        return JsonResponse({"error": "Salle de chat introuvable"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def get_conversation(request, room_code, token):
    # Fetch the token object and associated user
    token_obj = TokenForDoctor.objects.filter(token=token).first() or Token.objects.filter(token=token).first()
    if not token_obj:
        return Response({"error": "Invalid or expired token"}, status=400)

    user_obj = token_obj.user

    # Fetch the room based on the room_code
    room = get_object_or_404(Room, code=room_code)
    
    # Get messages related to the room, ordered by date
    messages = Message.objects.filter(room=room).order_by('date')
    
    # Update 'seen' status for each message where the receiver is the user associated with the token
    messages.filter(receiver=user_obj.id).update(seen=True)
    
    # Prepare the data for JSON response
    messages_data = [{
        'id': message.id,
        'value': message.value,
        'sender': message.sender,
        'receiver': message.receiver,
        'seen': message.seen,
        'date': message.date.strftime('%Y-%m-%d %H:%M:%S')
    } for message in messages]

    return Response(messages_data)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def get_unread_messages(request, token):
    # Attempt to fetch the token object for either a Doctor or a generic User
    token_obj = TokenForDoctor.objects.filter(token=token).first() or Token.objects.filter(token=token).first()
    if not token_obj:
        return JsonResponse({"error": "Invalid or expired token"}, status=400)

    # Identify the user object from the token
    user_obj = token_obj.user

    # Retrieve messages where 'seen' is False and 'receiver' matches the user ID from the token
    unread_messages = Message.objects.filter(receiver=user_obj.id, seen=False).order_by('date')

    # Serialize the messages data
    messages_data = [{
        'id': message.id,
        'value': message.value,
        'sender': message.sender,
        'receiver': message.receiver,
        'seen': message.seen,
        'date': message.date.strftime('%Y-%m-%d %H:%M:%S')
    } for message in unread_messages]

    return JsonResponse(messages_data, safe=False)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def getmessage(request, room,token):
    token = TokenForDoctor.objects.filter( token=token).exists()

    try:
        room_details = Room.objects.get(code=room)
        messages = Message.objects.filter(room=room_details).order_by('date')
        return JsonResponse({'messages': list(messages.values())}, status=200)
    except Room.DoesNotExist:
        return JsonResponse({'error': 'La salle spécifiée n\'existe pas'}, status=404)
    

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def getChatPatient(request, token):
    token_obj = Token.objects.filter(token=token).first()

    if request.method == 'GET':
        if token_obj:
            patient_obj = token_obj.user
            rooms = Room.objects.filter(patient=patient_obj)

            # Extract all fields for each room
            room_data = [{
                'code': room.code,
                'patient_id': room.patient.id,
                'patient_name': room.patient.username,  # Assuming 'username' is a field on the User model
                'medecin_id': room.medecin.id,
                'medecin_name': room.medecin.username  # Same assumption as above
            } for room in rooms]

            return JsonResponse({"rooms": room_data})
        else:
            return JsonResponse({"error": "Token invalide"}, status=400)

    return JsonResponse({"error": "Requête GET requise"}, status=400)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def getChatMedecin(request, token):
    token_obj = TokenForDoctor.objects.filter(token=token).first()

    if request.method == 'GET':
        if token_obj:
            medecin_obj = token_obj.user
            rooms = Room.objects.filter(medecin=medecin_obj)

            # Extract all fields for each room
            room_data = [{
                'code': room.code,
                'patient_id': room.patient.id,
                'patient_name': room.patient.username,  # Assuming 'username' is a field on the User model
                'medecin_id': room.medecin.id,
                'medecin_name': room.medecin.username  # Same assumption as above
            } for room in rooms]

            return JsonResponse({"rooms": room_data})
        else:
            return JsonResponse({"error": "Token invalide"}, status=400)

    return JsonResponse({"error": "Requête GET requise"}, status=400)

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user, seen=False)