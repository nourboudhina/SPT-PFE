from random import randint
from django.http import HttpResponse, JsonResponse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from account.models import User, Medecin, TokenForAgent
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes
from account.models import Token, TokenForDoctor
from .models import RendezVous


@csrf_exempt 
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def ajout_rendez_vous_par_agent(request , token) : 
        token = TokenForAgent.objects.filter(token=token).first()
        if request.method == 'POST':
            date_de_rdv = request.data.get('date_de_rdv')
            medecin = request.data.get('medecin')
            patient = request.data.get('patient')
            dateExist = RendezVous.objects.filter(date_rendez_vous = date_de_rdv)
            medecinExist = Medecin.objects.filter(username = medecin).exists()
            patientExist = User.objects.filter(username = patient)
            
            if not(dateExist) and patientExist and medecinExist : 
               rdv =  RendezVous.objects.create(date_rendez_vous = date_de_rdv,patient = patient , medecin = medecin)
               rdv.save()
               return JsonResponse({'success': 'Rendez-vous ajouté avec succès'}, status=201)

            elif dateExist and patientExist and medecinExist : 
                return JsonResponse({'erreur rendez-vous': 'Rendez vous avec ce medecin et ce patient existe déja'}, status=400)
            else : 
                return JsonResponse({'Donnee erreur ': 'Il y a quelque donnees manquante'}, status=400)
        else : 
            return JsonResponse({"error": "Invalid request method"}, status=405)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def getRendezVousDoctor(request, token):
    token_obj = TokenForDoctor.objects.filter(token=token).first()
    if request.method == 'GET':
        if token_obj:
            user_obj = token_obj.user
            username_medecin = user_obj.username
            date_rdv = RendezVous.objects.filter(medecin = username_medecin )
            user_data = {
                'username': username_medecin,
                'date_rdv' : date_rdv
            }
            return JsonResponse(user_data)
        else:
            return JsonResponse({"error": "Token invalide"}, status=400)
        
        
        
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def getRendezVousPatient(request, token):
    token_obj = Token.objects.filter(token=token).first()
    if request.method == 'GET':
        if token_obj:
            user_obj = token_obj.user
            username_patient = user_obj.username
            date_rdv = RendezVous.objects.filter(patient = username_patient )
            user_data = {
                'username': username_patient,
                'date_rdv' : date_rdv
            }
            return JsonResponse(user_data)
        else:
            return JsonResponse({"error": "Token invalide"}, status=400)
