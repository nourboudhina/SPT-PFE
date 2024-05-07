from random import randint
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from account.models import TokenForDoctor,Token, TokenForAgent
from rest_framework.decorators import api_view
from rest_framework.decorators import api_view, authentication_classes
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .models import PageAcceuil
from rest_framework.response import Response
from django.shortcuts import get_object_or_404,redirect
import base64
from django.views.decorators.csrf import csrf_exempt
from account.models import Medecin, Service, Specialite, Grade, Groupe
from django.shortcuts import render


@csrf_exempt
def pageA(request, token):
    token = TokenForDoctor.objects.filter(token=token).exists() if token else Token.objects.filter(token=token).exists()
    return render(request, 'Accueil/PageAccueil.html')   

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def getPageAcceuil(request, token):
    token_obj = TokenForDoctor.objects.filter(token=token).exists() if token else Token.objects.filter(token=token).exists()
    if request.method == 'GET':
        if token_obj:
            page_acceuil_data = PageAcceuil.objects.values() 
            for data in page_acceuil_data:
                postwithimage_path = data['postwithimage']
                with open(postwithimage_path, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                data['postwithimage'] = encoded_string  
            return JsonResponse(list(page_acceuil_data), safe=False)  
        else:
            return JsonResponse({"error": "Token invalide"}, status=400)
        
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
            date_naiss_patient = user_obj.date_naiss
            adresse_patient = user_obj.addresse
            gouvernorat_patient = user_obj.gouvernorat
            nationalite_patient = user_obj.nationalite
            image_path = user_obj.image.path
            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            user_data = {
                'username': username_patient,
                'email': email_patient,
                'phone': phone_patient,
                'fullname': fullname_patient,
                'date_naiss':date_naiss_patient,
                'adresse': adresse_patient,
                'gouvernorat':gouvernorat_patient ,
                'nationalite': nationalite_patient,
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
            username_medecin = user_obj.username
            email_medecin = user_obj.email
            phone_medecin = user_obj.phone
            fullname_medecin = user_obj.fullname
            date_naiss_medecin = user_obj.date_nais
            gouvernorat_medecin = user_obj.gouvernorat
            nationalite_medecin = user_obj.nationalite
            groupe_medecin = user_obj.groupe
            grade_medecin = user_obj.grade
            sepcialite_medecin = user_obj.sepcialite
            service_medecin = user_obj.service
            hopitale_medecin = user_obj.hopitale
            image_path = user_obj.image.path
            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            
            user_data = {
                'username': username_medecin,
                'email': email_medecin,
                'phone': phone_medecin,
                'fullname': fullname_medecin,
                'date_naiss':date_naiss_medecin,
                'gouvernorat':gouvernorat_medecin ,
                'nationalite': nationalite_medecin,
                'groupe':groupe_medecin ,
                'grade': grade_medecin,
                'sepcialite': sepcialite_medecin,
                'service':service_medecin ,
                'hopitale': hopitale_medecin,
                'image': encoded_string
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
            email_agent = user_obj.email
            phone_agent = user_obj.phone
            fullname_agent = user_obj.fullname
            date_naiss_agent = user_obj.date_naiss
            adresse_agent= user_obj.addresse
            gouvernorat_agent = user_obj.gouvernorat
            nationalite_agent = user_obj.nationalite
            hopitale_agent = user_obj.hopitale
            image_path = user_obj.image.path
            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            
            user_data = {
                'username': username_agent,
                'email': email_agent,
                'phone': phone_agent,
                'fullname': fullname_agent,
                'date_naiss':date_naiss_agent,
                'adresse': adresse_agent,
                'gouvernorat':gouvernorat_agent ,
                'nationalite': nationalite_agent,
                'hopitale': hopitale_agent,
                'image': encoded_string
            }

            
            return JsonResponse(user_data)
        else:
            return JsonResponse({"error": "Token invalide"}, status=400)
        
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def gestion_agent(request, token):
    if request.method == "POST":
        token_agent = TokenForAgent.objects.filter(token=token).first()
        agent = token_agent.user
        if agent:
            hopital = agent.hopitale
            services = Service.objects.filter(hopitale=hopital)

            specialites = Specialite.objects.filter(service__in=services)

            medecins = Medecin.objects.filter(hopitale=hopital)

           
            groupes = list(medecins.values_list('groupe__groupe', flat=True))

            return Response({
                'services': [service.service for service in services],
                'specialites': [specialite.specialite for specialite in specialites],
                'grades': [medecin.grade.grade for medecin in medecins],  # Access gradee field
                'groupes': groupes
            })
        else:
            return Response({'message': 'Agent non trouvé'}, status=400)
        
@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def delete_service(request, token,id):
    if request.method == "DELETE":
        service = get_object_or_404(Service,pk=id)
        token_agent = TokenForAgent.objects.filter(token = token).first()
        agent = token_agent.user
        if service.hopitale.id == agent.hopitale.id:  # Check if agent belongs to the same hospital
            service.delete()
            return Response({'message': 'Service supprimé avec succès'})
        else:
            return Response({'message': 'Vous ne pouvez pas supprimer un service d\'un autre hôpital'}, status=403)
        
        
@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def delete_specialite(request, token,id):
    if request.method == "DELETE":
        specialite = get_object_or_404(Specialite, pk=id)
        token_agent = TokenForAgent.objects.filter(token = token).first()
        agent = token_agent.user
        if specialite.service.hopitale.id == agent.hopitale.id:
            specialite.delete()
            return Response({'message': 'Spécialité supprimée avec succès'})
        else:
            return Response({'message': 'Vous ne pouvez pas supprimer une spécialité d\'un autre hôpital'}, status=403)
        
@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def delete_medecin(request, token,id):
    if request.method == "DELETE":
        medecin = get_object_or_404(Medecin, pk=id)
        token_agent = TokenForAgent.objects.filter(token = token).first()
        agent = token_agent.user
        if medecin.hopitale.id == agent.hopitale.id:
            medecin.delete()
            return Response({'message': 'Médecin supprimé avec succès'})
        else:
            return Response({'message': 'Vous ne pouvez pas supprimer un médecin d\'un autre hôpital'}, status=403)
        
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def add_service(request, token):
    if request.method == "POST":
        token_agent = TokenForAgent.objects.filter(token=token).first()
        agent = token_agent.user
        if agent:
            hopital = agent.hopitale
            data = request.data

            service_name = data.get('service')
            if not service_name:
                return Response({'message': 'Le nom du service est obligatoire'}, status=400)

            # Check if service with the same name already exists in the hospital
            existing_service = Service.objects.filter(hopitale=hopital, service=service_name ).first()
            if existing_service:
                return Response({'message': 'Un service avec ce nom existe déjà dans cet hôpital'}, status=400)

            # Create the new service
            new_service = Service.objects.create(hopitale=hopital, service=service_name)
            return Response({'message': 'Service ajouté avec succès', 'service': new_service.id})
        else:
            return Response({'message': 'Agent non trouvé'}, status=400)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def add_specialite(request, token):
    if request.method == "POST":
        token_agent = TokenForAgent.objects.filter(token=token).first()
        agent = token_agent.user
        if agent:
            hopital = agent.hopitale
            data = request.data

            service_id = data.get('service')
            specialite_name = data.get('specialite')

            if not service_id or not specialite_name:
                return Response({'message': 'Le service et la spécialité sont obligatoires'}, status=400)

            # Get the service object
            service = get_object_or_404(Service, pk=service_id, hopitale=hopital)

            # Check if specialty with the same name already exists in the service
            existing_specialite = Specialite.objects.filter(service=service, specialite=specialite_name).first()
            if existing_specialite:
                return Response({'message': 'Une spécialité avec ce nom existe déjà dans ce service'}, status=400)

            # Create the new specialty
            new_specialite = Specialite.objects.create(service=service, specialite=specialite_name)
            return Response({'message': 'Spécialité ajoutée avec succès', 'specialite': new_specialite.id})
        else:
            return Response({'message': 'Agent non trouvé'}, status=400)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def add_medecin(request, token):
    if request.method == "POST":
        token_agent = TokenForAgent.objects.filter(token=token).first()
        agent = token_agent.user
        if agent:
            hopital = agent.hopitale
            data = request.data

            groupe_id = data.get('groupe')
            grade_id = data.get('grade')
            specialite_id = data.get('specialite')
            service_id = data.get('service')
            username = data.get('username')
            password = data.get('password')

            if not (groupe_id and grade_id and specialite_id and service_id and username and password):
                return Response({'message': 'Tous les champs obligatoires ne sont pas renseignés'}, status=400)

            try:
                # Check for missing service
                if not service_id:
                    return Response({'message': 'Le service est obligatoire'}, status=400)

                # Get the groupe, grade, specialite, and service objects
                groupe = Groupe.objects.get(pk=groupe_id)
                grade = Grade.objects.get(pk=grade_id)
                specialite = Specialite.objects.get(pk=specialite_id)
                service = Service.objects.get(pk=service_id)

                if groupe and grade and specialite and service:
                    doctor = Medecin.objects.create(
                        username=username,
                        password=password,
                        hopitale=hopital,
                        groupe=groupe,
                        grade=grade,
                        sepcialite=specialite,
                        service=service  # Assign the retrieved service object
                    )
                    return Response({'message': 'Médecin ajouté avec succès', 'medecin': doctor.id})
            except (Groupe.DoesNotExist, Grade.DoesNotExist, Specialite.DoesNotExist, Service.DoesNotExist):
                return Response({'message': 'Groupe, grade, spécialité ou service introuvable'}, status=400)
            except Exception as e:  # Catch other potential errors
                return Response({'message': f'Une erreur est survenue: {str(e)}'}, status=500)

        else:
            return Response({'message': 'Agent non trouvé'}, status=400)
        
        
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def modify_medecin(request, token):
    if request.method == "POST":
        token_agent = TokenForAgent.objects.filter(token=token).first()
        agent = token_agent.user
        if agent:
            hopital = agent.hopitale
            data = request.data

            medecin_id = data.get('medecin')
            garde_id = data.get('garde')
            groupe_id = data.get('groupe')
            username = data.get('username')

            if not (medecin_id and (garde_id or groupe_id or username)):
                return Response({'message': 'Veuillez renseigner au moins un champ à modifier'}, status=400)

            try:
                # Get the doctor object
                medecin = Medecin.objects.get(pk=medecin_id)

                # Check if the doctor belongs to the agent's hospital
                if medecin.hopitale != hopital:
                    return Response({'message': 'Vous ne pouvez pas modifier un médecin d\'un autre hôpital'}, status=400)

                # Update fields based on provided values
                if garde_id:
                    medecin.grade = garde_id
                if groupe_id:
                    medecin.groupe = groupe_id
                if username:
                    medecin.username = username

                medecin.save()
                return Response({'message': 'Médecin modifié avec succès'})
            except Medecin.DoesNotExist:
                return Response({'message': 'Médecin introuvable'}, status=400)
            except Exception as e:
                return Response({'message': f'Une erreur est survenue: {str(e)}'}, status=500)

        else:
            return Response({'message': 'Agent non trouvé'}, status=400)

