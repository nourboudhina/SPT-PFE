from random import randint
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from account.models import User, Medecin, TokenForAgent
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes
from account.models import Token, TokenForDoctor
from django.utils import timezone
from .models import RendezVous, Apc, payment
from django.core.mail import send_mail
from celery import shared_task
from django.db.models import Count
from datetime import datetime

@shared_task
def envoyer_rappel_rendez_vous(request):
    aujourd_hui = timezone.now().date()
    demain = aujourd_hui + timezone.timedelta(days=1)

    rendez_vous_demain = RendezVous.objects.filter(date_rendez_vous=demain)

    for rendez_vous in rendez_vous_demain:
        
        patient = rendez_vous.patient

        message = f"""
        Rappel de rendez-vous:

        Patient: {patient.username}
        Médecin: {rendez_vous.medecin.username}
        Date: {rendez_vous.date_rendez_vous}

        N'oubliez pas votre rendez-vous !
        """

        send_mail(
            "Rappel de rendez-vous",
            message,
            "elyesmlik307@gmail.com",
            [patient.email],
            fail_silently=False
        )

        data = {
            "message": message
        }

        return JsonResponse(data)

    data = {
        "message": "Aucun rendez-vous n'est prévu pour demain."
    }
    return JsonResponse(data)


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
            username_patient = user_obj.username

            upcoming_rendez_vous = RendezVous.objects.filter(
                medecin=username_patient,
                date__gt=timezone.now().date()  
            )

            user_data = {
                'username': username_patient,
                'rendez_vous': list(upcoming_rendez_vous.values())  
            }

            return JsonResponse(user_data)
        else:
            return JsonResponse({"error": "Token invalide"}, status=400)
        
        
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def getRendezVousHDoctor(request, token):
    token_obj = TokenForDoctor.objects.filter(token=token).first()

    if request.method == 'GET':
        if token_obj:
            user_obj = token_obj.user
            username_patient = user_obj.username

            past_rendez_vous = RendezVous.objects.filter(
                medecin=username_patient,
                date__lt=timezone.now().date() 
            )

            user_data = {
                'username': username_patient,
                'rendez_vous': list(past_rendez_vous.values())  # Optimized for efficiency
            }

            return JsonResponse(user_data)
        else:
            return JsonResponse({"error": "Token invalide"}, status=400)
        
        
        
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def getRendezVousHPatient(request, token):
    token_obj = Token.objects.filter(token=token).first()

    if request.method == 'GET':
        if token_obj:
            user_obj = token_obj.user
            username_patient = user_obj.username

            past_rendez_vous = RendezVous.objects.filter(
                patient__username=username_patient,
                date__lt=timezone.now().date() 
            )
            past_apc = Apc.objects.filter(
                patient__username=username_patient,
                date__gt=timezone.now().date()  
            )

            user_data = {
                'username': username_patient,
                'rendez_vous': list(past_rendez_vous.values()) ,
                'apc' : list(past_apc.values())
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

            upcoming_rendez_vous = RendezVous.objects.filter(
                patient__username=username_patient,
                date__gt=timezone.now().date()  
            )
            upcoming_apc = Apc.objects.filter(
                patient__username=username_patient,
                date__gt=timezone.now().date()  
            )

            user_data = {
                'username': username_patient,
                'rendez_vous': list(upcoming_rendez_vous.values()) ,
                'apc' : list(upcoming_apc.values()) , 
            }

            return JsonResponse(user_data)
        else:
            return JsonResponse({"error": "Token invalide"}, status=400)


        
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def getPaiementHistorique(request, token):
    token_obj = Token.objects.filter(token=token).first()
    if request.method == 'GET':
        if token_obj:
            user_obj = token_obj.user
            username_email = user_obj.email
            paiements = payment.objects.filter(patient__email = username_email )
            paiements_data = []
            for paiement in paiements:
                paiement_data = {
                    "montant": paiement.payé,
                    "date": paiement.date,  
                }
                paiements_data.append(paiement_data)
            
            # Renvoyer la liste des paiements sous forme de réponse JSON
            return JsonResponse(paiements_data, safe=False)
        else:
            return JsonResponse({"error": "Token invalide"}, status=400)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def suivi_apc(request, token):
    if request.method == 'POST':
        token = TokenForDoctor.objects.filter(token=token).first()
        if token:
            month = request.data.get("month")
            month_date = datetime.strptime(month, "%Y-%m")
            
            rendez_vous = RendezVous.objects.filter(date_rendez_vous__year=month_date.year,
                                                     date_rendez_vous__month=month_date.month)
            apc = Apc.objects.filter(date__year=month_date.year,
                                     date__month=month_date.month)
            
            total_patients = rendez_vous.aggregate(num_patients=Count('patient'))['num_patients'] + \
                             apc.aggregate(num_patients=Count('patient'))['num_patients']
            
           
            rendez_vous_list = [rv.id for rv in rendez_vous]
            apc_list = [a.id for a in apc]
            
            return Response({
                'rendez_vous': rendez_vous_list,
                'apc': apc_list,
                'total_patients': total_patients
            })
        

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def get_agent_rendezvous_apc(request, token):
    if request.method == "GET":
        token_agent = TokenForAgent.objects.filter(token=token).first()
        agent = token_agent.user
        if agent:
            hopital = agent.hopital

            # Get all appointments for the agent's hospital
            rendez_vous = RendezVous.objects.filter(medecin__hopitale=hopital)
            apc = Apc.objects.filter(medecin__hopitale=hopital)

            # Prepare data for response
            rendez_vous_data = []
            for rv in rendez_vous:
                rendez_vous_data.append({
                    "id": rv.id,
                    "date_rendez_vous": rv.date_rendez_vous.strftime("%Y-%m-%d"),  # Format date
                    "patient": rv.patient.username,  # Assuming username for patient identification
                    "medecin": rv.medecin.username,  # Assuming username for doctor identification
                })

            apc_data = []
            for a in apc:
                apc_data.append({
                    "id": a.id,
                    "date": a.date.strftime("%Y-%m-%d %H:%M:%S"),  # Format date and time
                    "patient": a.patient.username,  # Assuming username for patient identification
                    "medecin": a.medecin.username,  # Assuming username for doctor identification
                })

            return Response({
                "rendez_vous": rendez_vous_data,
                "apc": apc_data,
            })
        else:
            return Response({'message': 'Agent non trouvé'}, status=400)


@api_view(['PUT'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def updateRendezVousDateD(request, token, rendez_vous_id):
    token_obj = TokenForDoctor.objects.filter(token=token).first()

    if request.method == 'PUT':
        if token_obj:
            try:
                rendez_vous = RendezVous.objects.get(pk=rendez_vous_id)
                print(rendez_vous)
            except RendezVous.DoesNotExist:
                return JsonResponse({"error": "Rendez-vous inexistant"}, status=404)
            new_date = request.data.get('new_date')
            if not new_date:
                return JsonResponse({"error": "Date de rendez-vous requise"}, status=400)

            try:
                new_date = datetime.datetime.strptime(new_date, '%Y-%m-%d').date()
            except ValueError:
                return JsonResponse({"error": "Format de date invalide"}, status=400)

            rendez_vous.date_rendez_vous = new_date
            rendez_vous.save()

            return JsonResponse({"message": "Date de rendez-vous mise à jour avec succès"})
        else:
            return JsonResponse({"error": "Token invalide"}, status=400)
        
        
@api_view(['PUT'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def updateRendezVousDateA(request, token, rendez_vous_id):
    token_obj = TokenForAgent.objects.filter(token=token).first()
    if request.method == 'PUT':
        if token_obj:
            try:
                rendez_vous = RendezVous.objects.get(pk=rendez_vous_id)
                print(rendez_vous)
            except RendezVous.DoesNotExist:
                return JsonResponse({"error": "Rendez-vous inexistant"}, status=404)
            new_date = request.data.get('new_date')
            if not new_date:
                return JsonResponse({"error": "Date de rendez-vous requise"}, status=400)
            try:
                new_date = datetime.datetime.strptime(new_date, '%Y-%m-%d').date()
            except ValueError:
                return JsonResponse({"error": "Format de date invalide"}, status=400)
            rendez_vous.date_rendez_vous = new_date
            rendez_vous.save()
            return JsonResponse({"message": "Date de rendez-vous mise à jour avec succès"})
        else:
            return JsonResponse({"error": "Token invalide"}, status=400)
        
        
@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def deleteRendezVousD(request, token, rendez_vous_id):
    token_obj = TokenForDoctor.objects.filter(token=token).first()

    if request.method == 'DELETE':
        if token_obj:
            try:
                rendez_vous = RendezVous.objects.get(pk=rendez_vous_id)
            except RendezVous.DoesNotExist:
                return JsonResponse({"error": "Rendez-vous inexistant"}, status=404)
            rendez_vous.delete()

            return JsonResponse({"message": "Rendez-vous supprimé avec succès"})
        else:
            return JsonResponse({"error": "Token invalide"}, status=400)
        
        
@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def deleteRendezVousA(request, token, rendez_vous_id):
    token_obj = TokenForAgent.objects.filter(token=token).first()

    if request.method == 'DELETE':
        if token_obj:
            try:
                rendez_vous = RendezVous.objects.get(pk=rendez_vous_id)
            except RendezVous.DoesNotExist:
                return JsonResponse({"error": "Rendez-vous inexistant"}, status=404)

            
            rendez_vous.delete()

            return JsonResponse({"message": "Rendez-vous supprimé avec succès"})
        else:
            return JsonResponse({"error": "Token invalide"}, status=400)
        

@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def getApcForAgent(request, token):
    token_obj = TokenForAgent.objects.filter(token=token).first()

    if request.method == 'POST':
        if token_obj:
            agent = token_obj.user
            hopital_agent = agent.hopital

            # Filter APC based on agent's hospital and matching doctor's hospital
            apc_list = Apc.objects.filter(
                hopital=hopital_agent,
                medecin__hopital=hopital_agent
            )

            # Convert APC objects to dictionaries for serialization (optional)
            apc_data = [apc.to_dict() for apc in apc_list]  # Assuming an 'to_dict' method in Apc

            # Get total count of matching APCs
            total_count = apc_list.count()

            return JsonResponse({
                "apc_data": apc_data,
                "total_count": total_count,
            })
        else:
            return JsonResponse({"error": "Token invalide"}, status=400)

    return JsonResponse({"error": "Requête POST requise"}, status=400) 


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def add_payment(request, token):
    token_obj = TokenForAgent.objects.filter(token=token).first()

    if request.method == 'POST':
        if token_obj:
            if request.data:
                try:
                    patient = token_obj.user
                    payé = request.data.get('payé')  

                    payment = payment.objects.create(patient=patient, payé=payé)
                    return JsonResponse({"message": "Paiement ajouté avec succès", "id": payment.id})
                except Exception as e:
                    return JsonResponse({"error": str(e)}, status=400)
            else:
                return JsonResponse({"error": "Données de paiement requises"}, status=400)
        else:
            return JsonResponse({"error": "Token invalide"}, status=400)

    return JsonResponse({"error": "Requête POST requise"}, status=400)


@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def delete_payment(request, token, payment_id):
    token_obj = TokenForAgent.objects.filter(token=token).first()

    if request.method == 'DELETE':
        if token_obj:
            try:
                payment = payment.objects.get(pk=payment_id)
                payment.delete()
                return JsonResponse({"message": "Paiement supprimé"})
            except payment.DoesNotExist:
                return JsonResponse({"error": "Paiement introuvable"}, status=404)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=400)
        else:
            return JsonResponse({"error": "Token invalide"}, status=400)

    return JsonResponse({"error": "Requête DELETE requise"}, status=400)


@api_view(['PUT'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def update_payment(request, token, payment_id):
    token_obj = TokenForAgent.objects.filter(token=token).first()

    if request.method == 'PUT':
        if token_obj:
            if request.data:
                try:
                    payment = payment.objects.get(pk=payment_id)
                    payé = request.data.get('payé') 
                    payment.payé = payé
                    payment.save()
                    return JsonResponse({"message": "Paiement mis à jour"})
                except payment.DoesNotExist:
                    return JsonResponse({"error": "Paiement introuvable"}, status=404)
                except Exception as e:
                    return JsonResponse({"error": str(e)}, status=400)
            else:
                return JsonResponse({"error": "Données de paiement requises"}, status=400)
        else:
            return JsonResponse({"error": "Token invalide"}, status=400)

    return JsonResponse({"error": "Requête PUT requise"}, status=400)



