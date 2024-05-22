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
from .models import RendezVous, Apc, Payment
from django.core.mail import send_mail
from celery import shared_task
from django.db.models import Count
from datetime import datetime
from django.shortcuts import render
from datetime import datetime
import random
from account.serializers import PaymentSerializer

def convert_to_hex_with_prefix(seconds):
    # Generate a random uppercase letter
    prefix = chr(random.randint(ord('A'), ord('Z')))
    # Extract the integer part before the decimal
    integer_part = int(seconds)
    # Convert integer part to hexadecimal
    hex_value = format(integer_part, 'X')
    # Return the combined string
    return f"{prefix}{hex_value}"
@csrf_exempt
def SAPCPage(request, token):
    token = TokenForDoctor.objects.filter(token=token).exists() if token else Token.objects.filter(token=token).exists()
    return render(request, 'Historique/SuivieAPC.html')  


@csrf_exempt
def GAPC(request, token):
    token = TokenForDoctor.objects.filter(token=token).exists() if token else Token.objects.filter(token=token).exists()
    return render(request, 'Gestion/GestionAPC.html')
@csrf_exempt
def GPy(request, token):
    token = TokenForDoctor.objects.filter(token=token).exists() if token else Token.objects.filter(token=token).exists()
    return render(request, 'Gestion/GestionPay.html')
@csrf_exempt
def GRDV(request, token):
    token = TokenForDoctor.objects.filter(token=token).exists() if token else Token.objects.filter(token=token).exists()
    return render(request, 'Gestion/GestionRDV.html')      
@csrf_exempt
def planingP(request, token):
    token = TokenForDoctor.objects.filter(token=token).exists() if token else Token.objects.filter(token=token).exists()
    return render(request, 'Planning/PlanningPatient.html')   
@csrf_exempt
def planingM(request, token):
    token = TokenForDoctor.objects.filter(token=token).exists() 
    if token:
        return render(request, 'Planning/PlanningMed.html')   
@csrf_exempt
def HRdvP(request, token):
    token = Token.objects.filter(token=token).exists() 
    if token:
        return render(request, 'Historique/HistoriqueRDVPa.html')   
@csrf_exempt
def HRdvM(request, token):
    token = TokenForDoctor.objects.filter(token=token).exists() 
    if token:
        return render(request, 'Historique/HistoriqueRDVMed.html')   
@csrf_exempt
def HAPCP(request, token):
    token = Token.objects.filter(token=token).exists() 
    if token:
        return render(request, 'Historique/HistoriqueAPCPa.html')   
@csrf_exempt
def HAPCM(request, token):
    token = TokenForDoctor.objects.filter(token=token).exists() 
    if token:
        return render(request, 'Historique/HistoriqueAPCMed.html')   
@csrf_exempt
def HpayP(request, token):
    token = Token.objects.filter(token=token).exists() 
    if token:
        return render(request, 'Historique/HistoriquePayPa.html')   
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
            "nourboudhina19@gmail.com",
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
            try:
                now = datetime.now()
                midnight = datetime.combine(now.date(), datetime.min.time())
                date_de_rdv = request.data.get('date_de_rdv')
                print(date_de_rdv)
                medecin = request.data.get('medecin')
                
                patient = request.data.get('patient')
                print(patient)
                id=convert_to_hex_with_prefix((now - midnight).total_seconds() )
                dateExist = RendezVous.objects.filter(date_rendez_vous = date_de_rdv)
                medecinExist = Medecin.objects.filter(id = medecin).exists()
                patientExist = User.objects.filter(id = patient)
                print(patientExist)
                if not(dateExist) and patientExist and medecinExist : 
                    patientobj=User.objects.filter(id=patient).first()
                    medobj=Medecin.objects.filter(id=medecin).first()
                    rdv =  RendezVous.objects.create(id=id,date_rendez_vous = date_de_rdv,patient = patientobj, medecin = medobj)
                    rdv.save()
                    return JsonResponse({'success': 'Rendez-vous ajouté avec succès'}, status=201)

                elif dateExist and patientExist and medecinExist : 
                    return JsonResponse({'erreur rendez-vous': 'Rendez vous avec ce medecin et ce patient existe déja'}, status=400)
                else : 
                    return JsonResponse({'Donnee erreur ': 'Il y a quelque donnees manquante'}, status=400)
            except Exception as e:
                print(e)
        else : 
            return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt 
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def ajout_APC_par_agent(request , token) : 
        token = TokenForAgent.objects.filter(token=token).first()
        now = datetime.now()
        midnight = datetime.combine(now.date(), datetime.min.time())
        if request.method == 'POST':
            date_de_apc = request.data.get('date_de_apc')
            print(date_de_apc)
            medecin = request.data.get('medecin')
            patient = request.data.get('patient')
            dateExist = Apc.objects.filter(date = date_de_apc)
            medecinExist = Medecin.objects.filter(id = medecin).exists()
            patientExist = User.objects.filter(id = patient)
            id=convert_to_hex_with_prefix((now - midnight).total_seconds() )
            if not(dateExist) and patientExist and medecinExist : 
                patientobj=User.objects.filter(id=patient).first()
                medobj=Medecin.objects.filter(id=medecin).first()
                apc =  Apc.objects.create( id=id,date = date_de_apc,patient = patientobj , medecin = medobj)
                apc.save()
                return JsonResponse({'success': 'Consultation APC ajouté avec succès'}, status=201)

            elif dateExist and patientExist and medecinExist : 
                return JsonResponse({'erreur APC': 'Consultation APC avec ce medecin et ce patient existe déja'}, status=400)
            else : 
                return JsonResponse({'Donnee erreur ': 'Il y a quelque donnees manquante'}, status=400)
        else : 
            return JsonResponse({"error": "Invalid request method"}, status=405)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def get_Planning_Doctor(request, token):
    token_obj = TokenForDoctor.objects.filter(token=token).first()
    print(token_obj)
    if request.method == 'GET':
        if token_obj:
            user_obj = token_obj.user
            print(user_obj)
            username_medecin = user_obj.username

            upcoming_rendez_vous = RendezVous.objects.filter(
                medecin=user_obj,
                date_rendez_vous__gt=timezone.now().date()  
            )

            upcoming_apc = Apc.objects.filter(
                medecin=user_obj,
                date__gt=timezone.now().date()  
            )

            user_data = {
                'username': username_medecin,
                'rendez_vous': list(upcoming_rendez_vous.values()),
                'apc': list(upcoming_apc.values())  
            }

            return JsonResponse(user_data)
        else:
            return JsonResponse({"error": "Token invalide"}, status=400)
        
        
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def get_RendezVousH_Doctor(request, token):
    token_obj = TokenForDoctor.objects.filter(token=token).first()

    if request.method == 'GET':
        if token_obj:
            user_obj = token_obj.user
            username_medecin = user_obj.username

            past_rendez_vous = RendezVous.objects.filter(
                medecin=user_obj,
                date_rendez_vous__lt=timezone.now().date() 
            )

            user_data = {
                'username': username_medecin,
                'rendez_vous': list(past_rendez_vous.values())
            }

            return JsonResponse(user_data)
        else:
            return JsonResponse({"error": "Token invalide"}, status=400)
        
        
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def get_APCH_Doctor(request, token):
    token_obj = TokenForDoctor.objects.filter(token=token).first()

    if request.method == 'GET':
        if token_obj:
            user_obj = token_obj.user
            username_medecin = user_obj.username

            past_apc = Apc.objects.filter(
                medecin=user_obj,
                date__lt=timezone.now().date()  
            )

            user_data = {
                'username': username_medecin,  
                'apc' : list(past_apc.values())
            }

            return JsonResponse(user_data)
        else:
            return JsonResponse({"error": "Token invalide"}, status=400)   
        
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def get_RendezVousH_Patient(request, token):
    token_obj = Token.objects.filter(token=token).first()

    if request.method == 'GET':
        if token_obj:
            user_obj = token_obj.user
            username_patient = user_obj.username

            past_rendez_vous = RendezVous.objects.filter(
                patient__username=username_patient,
                date_rendez_vous__lt=timezone.now().date() 
            )
            

            user_data = {
                'username': username_patient,
                'rendez_vous': list(past_rendez_vous.values()) ,
                
            }

            return JsonResponse(user_data)
        else:
            return JsonResponse({"error": "Token invalide"}, status=400)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def get_APCH_Patient(request, token):
    token_obj = Token.objects.filter(token=token).first()

    if request.method == 'GET':
        if token_obj:
            user_obj = token_obj.user
            username_patient = user_obj.username

            past_apc = Apc.objects.filter(
                patient__username=username_patient,
                date__gt=timezone.now().date()  
            )

            user_data = {
                'username': username_patient,
                'apc' : list(past_apc.values())
            }

            return JsonResponse(user_data)
        else:
            return JsonResponse({"error": "Token invalide"}, status=400)
        

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def get_Planning_Patient(request, token):
    token_obj = Token.objects.filter(token=token).first()

    if request.method == 'GET':
        if token_obj:
            user_obj = token_obj.user
            username_patient = user_obj.username

            upcoming_rendez_vous = RendezVous.objects.filter(
                patient__username=username_patient,
                date_rendez_vous__gt=timezone.now().date()  
            )
            print(upcoming_rendez_vous.values)
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
def get_PaiementHistorique(request, token):
    token_obj = Token.objects.filter(token=token).first()
    if request.method == 'GET':
        if token_obj:
            user_obj = token_obj.user
            username_email = user_obj.email
            paiements = Payment.objects.filter(patient__email = username_email )
            paiements_data = []
            for paiement in paiements:
                paiement_data = {
                    "id":paiement.id,
                    "montant": paiement.payé,
                    "date": paiement.date,  
                }
                paiements_data.append(paiement_data)
            
           
            return JsonResponse(paiements_data, safe=False)
        else:
            return JsonResponse({"error": "Token invalide"}, status=400)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def suivi_apc(request, token):
    if request.method == 'GET':
        token = TokenForDoctor.objects.filter(token=token).first()
        if token:
            month = request.data.get("month")
            month_date = datetime.strptime(month, "%Y-%m")
            
            apc = Apc.objects.filter(date__year=month_date.year,
                                     date__month=month_date.month)
            
            total_patients = apc.aggregate(num_patients=Count('patient'))['num_patients']
            
           
            
            apc_list = [{'id': a.id, 'date': a.date.strftime('%Y-%m-%d')} for a in apc]
            
            return Response({
                'apc': apc_list,
                'total_patients': total_patients
            })
        

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def get_agent_rendezvous_apc(request, token):
    if request.method == "GET":
        print(token)
        token_agent = TokenForAgent.objects.filter(token=token).first()
        print(token_agent)
        agent = token_agent.user
        if agent:
            hopital = agent.hopitale

            # Get all appointments for the agent's hospital
            rendez_vous = RendezVous.objects.filter(medecin__hopitale=hopital)
            apc = Apc.objects.filter(medecin__hopitale=hopital)

            # Prepare data for response
            rendez_vous_data = []
            for rv in rendez_vous:
                rendez_vous_data.append({
                    "id": rv.id,
                    "date_rendez_vous": rv.date_rendez_vous.strftime("%Y-%m-%d %H:%M"),  
                    "patient": rv.patient.fullname,  
                    "medecin": rv.medecin.username,  
                })

            apc_data = []
            for a in apc:
                apc_data.append({
                    "id": a.id,
                    "date": a.date.strftime("%Y-%m-%d %H:%M:%S"),  
                    "patient": a.patient.id,  
                    "medecin": a.medecin.id, 
                })

            return Response({
                "rendez_vous": rendez_vous_data,
                "apc": apc_data,
            })
        else:
            return Response({'message': 'Agent non trouvé'}, status=400)


@api_view(['PUT'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def update_D(request, token, type, id):
    token_obj = TokenForDoctor.objects.filter(token=token).first()

    if request.method == 'PUT':
        if token_obj:
            try:
                if type == 'RendezVous':
                    rendez_vous = RendezVous.objects.get(pk=id)
                elif type == 'Apc':
                    apc = Apc.objects.get(pk=id)
                else:
                    return JsonResponse({"error": "Type invalide"}, status=400)
            except (RendezVous.DoesNotExist, Apc.DoesNotExist):
                return JsonResponse({"error": "Objet inexistant"}, status=404)

            new_date = request.data.get('new_date')
            if not new_date:
                return JsonResponse({"error": "Date de rendez-vous requise"}, status=400)

            try:
                new_date = datetime.datetime.strptime(new_date, '%Y-%m-%d').date()
            except ValueError:
                return JsonResponse({"error": "Format de date invalide"}, status=400)

            if type == 'RendezVous':
                rendez_vous.date_rendez_vous = new_date
                rendez_vous.save()
                return JsonResponse({"message": "Date de rendez-vous mise à jour avec succès"})
            elif type == 'Apc':
                apc.date = new_date
                apc.save()
                return JsonResponse({"message": "Date de APC mise à jour avec succès"})
                pass
        else:
            return JsonResponse({"error": "Token invalide"}, status=400)
        
        
@api_view(['PUT'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def update_RendezVous_Date_A(request, token, rendez_vous_id):
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
            #try:
                #new_date = datetime.strptime(new_date, '%Y-%m-%d').date()
            #except ValueError:

                return JsonResponse({"error": "Format de date invalide"}, status=400)
            
            rendez_vous.date_rendez_vous = new_date
            
            rendez_vous.save()
            
            return JsonResponse({"message": "Date de rendez-vous mise à jour avec succès"})
        else:
            return JsonResponse({"error": "Token invalide"}, status=400)
        
        
@api_view(['PUT'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def update_APC_Date_A(request, token, apc_id):
    token_obj = TokenForAgent.objects.filter(token=token).first()
    if request.method == 'PUT':
        if token_obj:
            try:
                apc = Apc.objects.get(pk=apc_id)
                print(apc)
            except Apc.DoesNotExist:
                return JsonResponse({"error": "APC inexistant"}, status=404)
            new_date = request.data.get('new_date')
            if not new_date:
                return JsonResponse({"error": "Date de APC requise"}, status=400)
            #try:
                #new_date = datetime.datetime.strptime(new_date, '%Y-%m-%d').date()
            #except ValueError:
                #return JsonResponse({"error": "Format de date invalide"}, status=400)
            apc.date = new_date
            apc.save()
            return JsonResponse({"message": "Date de APC mise à jour avec succès"})
        else:
            return JsonResponse({"error": "Token invalide"}, status=400)
        

@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def delete_D(request, token, type, id):
    token_obj = TokenForDoctor.objects.filter(token=token).first()

    if request.method == 'DELETE':
        if token_obj:
            try:
                if type == 'RendezVous':
                    rendez_vous = RendezVous.objects.get(pk=id)
                elif type == 'Apc':
                    apc = Apc.objects.get(pk=id)
                else:
                    return JsonResponse({"error": "Type invalide"}, status=400)
            except (RendezVous.DoesNotExist, Apc.DoesNotExist):
                return JsonResponse({"error": " inexistant"}, status=404)

            if type == 'RendezVous':
                rendez_vous.delete()
                return JsonResponse({"message": "Rendez-vous supprimé avec succès"})
            elif type == 'Apc':
                apc.delete()
                return JsonResponse({"message": "APC supprimé avec succès"})
        else:
            return JsonResponse({"error": "Token invalide"}, status=400)
        
        
        
@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def delete_RendezVous_A(request, token, rendez_vous_id):
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
        
@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def delete_APC_A(request, token, apc_id):
    token_obj = TokenForAgent.objects.filter(token=token).first()

    if request.method == 'DELETE':
        if token_obj:
            try:
                apc = Apc.objects.get(pk=apc_id)
            except apc.DoesNotExist:
                return JsonResponse({"error": "APC inexistant"}, status=404)

            
            apc.delete()

            return JsonResponse({"message": "APC supprimé avec succès"})
        else:
            return JsonResponse({"error": "Token invalide"}, status=400)
        

@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def getApcForAgent(request, token):
    token_obj = TokenForAgent.objects.filter(token=token).first()

    if request.method == 'POST':
        if token_obj:
            agent = token_obj.user
            hopital_agent = agent.hopitale

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
            
            now = datetime.now()
            midnight = datetime.combine(now.date(), datetime.min.time())
            id=convert_to_hex_with_prefix((now - midnight).total_seconds() )
            print(token_obj)   
            patient = request.data.get('patient')
            payé = request.data.get('mount') 
            date = request.data.get('date') 
            patientobj=User.objects.filter(id=patient).first()
            patientExist = User.objects.filter(id=patient)
            print()
            if patientExist :
                try:
                    payment = Payment.objects.create(id=id,patient=patientobj, payé=payé, date=date)
                    payment.save()
                except Exception as e:
                    print(e)
                return JsonResponse({"message": "Paiement ajouté avec succès", "id": payment.id})
            elif patientExist : 
                return JsonResponse({'erreur APC': ' ce patient nexiste pas'}, status=400)
        else : 
            return JsonResponse({'Donnee erreur ': 'Il y a quelque donnees manquante'}, status=400)
        
    return JsonResponse({"error": "Invalid request method"}, status=405)


@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def delete_payment(request, token, payment_id):
    token_obj = TokenForAgent.objects.filter(token=token).first()

    if request.method == 'DELETE':
        if token_obj:
            try:
                payment = Payment.objects.get(id=payment_id)
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
                    payment = Payment.objects.get(id=payment_id)
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

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def list_payments(request,token):
    token_obj = TokenForAgent.objects.filter(token=token).first()

    if request.method == 'GET':
        if token_obj:
            payments = Payment.objects.all()
            serializer = PaymentSerializer(payments, many=True)
            return Response(serializer.data)
        else:
            return JsonResponse({"error": "Token invalide"}, status=400)
