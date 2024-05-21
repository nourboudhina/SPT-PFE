import datetime
import json
import logging
from random import randint
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404,redirect
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from account.models import Specialite, Otp, PasswordResetToken, Token, User, Medecin, TokenForDoctor, Agent, TokenForAgent ,Service 
from account.utils import IsAuthenticatedUser, send_otp, send_password_reset_email, token_response, token_response_Agent, token_response_doctor
from rest_framework.parsers import FormParser
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password,check_password
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie,csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import loader
from account.serializers import UserSerializer
from SoinsPourTous.settings import TEMPLATES_BASE_URL
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated ,DjangoModelPermissions,AllowAny
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http import Http404
from django.utils import timezone
from datetime import timedelta
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.decorators import login_required, permission_required
from rest_framework import permissions
from django.views.generic import TemplateView
from django.shortcuts import render
from .serializers import User_Serializer,ServiceSerializer
import uuid
from .serializers import MedecinSerializer, GradeSerializer ,GroupeSerializer,SpecialiteSerializer
from .models import Grade ,Groupe ,Gouvernorat
from .models import Nationalite

def list_nationalites(request):
    nationalites = Nationalite.objects.all()
    data = [{'id': n.id, 'nationalite': n.nationalite} for n in nationalites]
    return JsonResponse(data, safe=False)

def get_gouvernorats(request):
    # Extract the choices directly from the model's field choices
    choices = Gouvernorat._meta.get_field('options').choices
    data = [{'id': choice[0], 'name': choice[1]} for choice in choices]
    return JsonResponse(data, safe=False)
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def add_medecin(request):
    if request.method == 'POST':
        try:

            data = json.loads(request.body)
            id=data.get('id')
            username = data.get('username')
            email = data.get('email')
            groupe_id = data.get('groupe')
            grade_id = data.get('grade')
            specialite_id = data.get('specialite')
            service_id = data.get('service')
            hopitale_id = data.get('hopitale')
            phone = data.get('phone')
            fullname = data.get('fullname')
            print(fullname)
            addresse = data.get('addresse')
            token=data.get('token')
            gouvernorat_id = data.get('gouvernerat')
            print(gouvernorat_id)
            nationalite_id = data.get('nationalite')
            sexe = data.get('sexe')
            password = data.get('password')
            date_nais = data.get('date')
            addresse = data.get('addresse')
            # Retrieve related objects
            groupe = Groupe.objects.get(id=groupe_id)
            grade = Grade.objects.get(id=grade_id)
            specialite = Specialite.objects.get(id=specialite_id)
            print(specialite.id)
            service = Service.objects.get(id=service_id)
            #hopitale = Hopital.objects.get(id=hopitale_id)
            gouvernorat = get_object_or_404(Gouvernorat, options=gouvernorat_id)
            print(gouvernorat)
            nationalite = Nationalite.objects.get(id=nationalite_id)
            print (nationalite)
            token_agent = TokenForAgent.objects.filter(token=token).first()
            agent = token_agent.user
            # Create new Medecin instance
            medecin = Medecin(
                id=id,  # Assuming you have a function to generate unique IDs
                username=username,
                email=email,
                groupe=groupe,
                grade=grade,
                specialite=specialite,
                service=service,
                hopitale = agent.hopitale,
                phone=phone,
                fullname=fullname,
                addresse=addresse,
                gouvernorat=gouvernorat,
                nationalite=nationalite,
                #sexe=sexe,
                password=password,  # Make sure to hash the password in production
                date_nais=date_nais
            )
            medecin.save()
            return JsonResponse({'success': 'Medecin added successfully'}, status=201)

        except Exception as e:

            return JsonResponse({'message': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Invalid HTTP method'}, status=405)

@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def delete_medecin(request, pk):
    try:
        medecin = Medecin.objects.get(pk=pk)
        medecin.delete()
        return Response({'message': 'Médecin deleted successfully'}, status=204)
    except Medecin.DoesNotExist:
        return Response({'message': 'Médecin not found'}, status=404)
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def list_medecins(request):
    medecins = Medecin.objects.all()
    serializer = MedecinSerializer(medecins, many=True)
    return Response(serializer.data)
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def list_patient(request):
    patient = User.objects.all()
    serializer = User_Serializer(patient, many=True)
    return Response(serializer.data)   
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def list_groupes(request):
    groupes = Groupe.objects.all()
    serializer = GroupeSerializer(groupes, many=True)
    return Response(serializer.data)
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def list_grades(request):
    grades = Grade.objects.all()
    serializer = GradeSerializer(grades, many=True)
    return Response(serializer.data)
@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def delete_specialite(request, pk):
    try:
        specialite = Specialite.objects.get(pk=pk)
        specialite.delete()
        return Response({'message': 'Service deleted successfully'}, status=204)
    except Specialite.DoesNotExist:
        return Response({'message': 'Service not found'}, status=404)
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def add_specialiter(request):
    if request.method == 'POST':
       
        try:
            data = json.loads(request.body)
            specialite_name = data.get('specialite')
            service_id=data.get('service')
            id=data.get('id')
            try:
                service = Service.objects.get(id=service_id)
            except Exception as e:
                    print(e)    
            if specialite_name:
                # Assuming 'hopitale_id' needs to be provided or is fixed for this example
                 # Example: Get the first hospital
                try:
                    new_specialite = Specialite.objects.create(id=id, specialite=specialite_name, service=service)
                except Exception as e:
                    return JsonResponse({'message': str(e)}, status=201)
                new_specialite.save()
                return JsonResponse({'message': 'Service added successfully'}, status=201)
            else:
                return JsonResponse({'message': 'Missing service name'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Invalid HTTP method'}, status=405)


import base64
from django.core.files.base import ContentFile
from django.http import JsonResponse

@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def update_profile(request, token):
    if request.method == 'POST':
        # Attempt to retrieve the user from multiple token models
        user_obj = None
        for token_model in [Token, TokenForDoctor, TokenForAgent]:
            token_query = token_model.objects.filter(token=token)
            if token_query.exists():
                
                user_obj = token_query.first().user
                break
        print(user_obj.id)
        if user_obj:
            try:
                # Fetch related models based on ids provided in request data
                gouvernorat_id = request.data.get('gouvernorat')
                print(gouvernorat_id)
                nationalite_id = request.data.get('nationalite')
                gouvernorat = get_object_or_404(Gouvernorat, options=gouvernorat_id)
                print(gouvernorat )
                nationalite = Nationalite.objects.get(id=nationalite_id)
                if token_model == TokenForDoctor:
                    user_obj.date_nais = request.data.get('date_nais', user_obj.date_nais)
                    print('1')
                else:
                    user_obj.date_naiss = request.data.get('date_nais', user_obj.date_naiss)
                    print('2')
                # Update user attributes
                user_obj.email = request.data.get('email', user_obj.email)
                user_obj.username = request.data.get('username', user_obj.username)
                user_obj.phone = request.data.get('phone', user_obj.phone)
                user_obj.fullname = request.data.get('fullname', user_obj.fullname)
                user_obj.addresse = request.data.get('adresse', user_obj.addresse)
                user_obj.gouvernorat = gouvernorat
                user_obj.nationalite = nationalite
                user_obj.sexe = request.data.get('sexe', user_obj.sexe)
                print('3')

                # Handle image upload if provided in base64 format
                image_data = request.data.get('image')
                if image_data:
                    format, imgstr = image_data.split(';base64,')
                    ext = format.split('/')[-1]
                    image_file = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
                    user_obj.image.save(f'profile.{ext}', image_file, save=False)

                # Save the updated user object
                user_obj.save()
            except Exception as e:
                print(e)
            return JsonResponse({"message": "Profile updated successfully"}, status=200)
        else:
            return JsonResponse({"error": "Invalid or expired token"}, status=400)
    else:
        return JsonResponse({"error": "POST request required"}, status=405)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def edit_specialite(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            specialite_name = data.get('specialite')
            service_id = data.get('service')
            specialite_id = data.get('id')  # 'id' is optional for new specialities
            print(service_id)
            try:
                service = Service.objects.get(id=service_id)
            except Service.DoesNotExist:
                return JsonResponse({'message': 'Service not found'}, status=404)

            if not specialite_name:
                return JsonResponse({'message': 'Specialite name is required'}, status=400)

            if specialite_id:
                # Update existing specialite
                try:
                    specialite = Specialite.objects.get(id=specialite_id)
                    specialite.specialite = specialite_name
                    specialite.service = service
                    specialite.save()
                    return JsonResponse({'message': 'Specialite updated successfully'}, status=200)
                except Specialite.DoesNotExist:
                    return JsonResponse({'message': 'Specialite not found'}, status=404)
        

        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Invalid HTTP method'}, status=405)
@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def specialite_list(request):
    """
    List all specialites, or create a new specialite.
    """
    if request.method == 'GET':
        specialites = Specialite.objects.all()
        serializer = SpecialiteSerializer(specialites, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SpecialiteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def specialite_detail(request, pk):
    """
    Retrieve, update or delete a specialite.
    """
    try:
        specialite = Specialite.objects.get(pk=pk)
    except Specialite.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SpecialiteSerializer(specialite)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SpecialiteSerializer(specialite, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        specialite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def generate_unique_id():
    return str(uuid.uuid4())


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def edit_service(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            service_name = data.get('service')
            token = data.get('token')
            id = data.get('id')  # 'id' is optional for new services
            
            token_obj = TokenForAgent.objects.filter(token=token).first()
            if not token_obj:
                return JsonResponse({'error': 'Invalid token'}, status=400)

            user_obj = token_obj.user
            if not service_name:
                return JsonResponse({'error': 'Service name is required'}, status=400)

            if id:
                # Update existing service
                try:
                    service = Service.objects.get(id=id, hopitale=user_obj.hopitale)  # Ensure service belongs to user's hospital
                    service.service = service_name
                    service.save()
                    return JsonResponse({'success': 'Service updated successfully'}, status=200)
                except Service.DoesNotExist:
                    return JsonResponse({'error': 'Service not found'}, status=404)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)   
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def add_service(request):
    if request.method == 'POST':
       
        try:
            data = json.loads(request.body)
            service_name = data.get('service')
            token=data.get('token')
            id=data.get('id')
            token_obj = TokenForAgent.objects.filter(token=token).first()
            user_obj = token_obj.user
            print(user_obj.email)
            if service_name:
                # Assuming 'hopitale_id' needs to be provided or is fixed for this example
                 # Example: Get the first hospital
                try:
                    new_service = Service.objects.create(id=id, service=service_name, hopitale=user_obj.hopitale)
                except Exception as e:
                    print(e)   
                print(new_service.service)
                new_service.save()
                return JsonResponse({'success': 'Service added successfully'}, status=201)
            else:
                return JsonResponse({'error': 'Missing service name'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)
@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def delete_service(request, pk):
    try:
        service = Service.objects.get(pk=pk)
        service.delete()
        return Response({'message': 'Service deleted successfully'}, status=204)
    except Service.DoesNotExist:
        return Response({'error': 'Service not found'}, status=404)
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def list_services(request):
    services = Service.objects.all()
    serializer = ServiceSerializer(services, many=True)
    return Response(serializer.data)
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def list_Specialite(request):
    specialite = Specialite.objects.all()
    serializer = SpecialiteSerializer(specialite, many=True)
    return Response(serializer.data)      
class landing (TemplateView):
    template_name = 'Landing/LandingPage.html'
def Personnel(request):
    return render(request, 'Landing/Personnel.html')

def about(request):
    return render(request, 'Landing/About.html')

def contact(request):
    return render(request, 'Landing/Contact.html')


@csrf_exempt
def loginP(request):
    return render(request, 'Login/LoginPatient.html')

@csrf_exempt
def loginM(request):
    return render(request, 'Login/LoginMédecin.html')

@csrf_exempt
def loginA(request):
    return render(request, 'Login/LoginAgent.html')

@csrf_exempt
def Registration(request):
    return render(request, 'Registration/Registration.html')

@csrf_exempt
def Verif(request):
    return render(request, 'Verif/VerificationForm.html')

@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def request_otp(request):
    email = request.data.get('email')
    phone = request.data.get('phone')

    if email and phone:
        if not User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'username does not exist'}, status=400)

        if not User.objects.filter(phone=phone).exists():
            return JsonResponse({'error': 'Phone does not exist'}, status=400)

        return send_otp(phone)
    else:
        return JsonResponse({'error': 'Data missing'}, status=400)
    
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def resend_otp(request) : 
    phone = request.data.get('phone')
    if not phone : 
        return Response('data_missing',400)
    return send_otp(phone)


# Créer un objet logger
logger = logging.getLogger(__name__)
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def verify_otp(request):
    try:
        phone = request.data.get('phone')
        otp = request.data.get('otp')

        print(f"Received OTP: {otp}")
        print(f"Received phone: {phone}")

        if not phone or not otp:
            return JsonResponse({'error': 'Phone or OTP missing in the request'}, status=400)

        otp_obj = get_object_or_404(Otp, phone=phone, verified=False)

        
            # Si la validité n'est pas définie, créez une validité de 10 minutes à partir du temps actuel
        validity_duration = timedelta(minutes=10)
        otp_obj.validity = timezone.now() + validity_duration
        otp_obj.save()

        # Utilisez make_aware pour ajouter le fuseau horaire par défaut
        validity_datetime = timezone.make_aware(datetime.datetime.combine(otp_obj.validity, datetime.datetime.now().time()))

        print(f"Validity datetime: {validity_datetime}")
        print(f"Current datetime: {timezone.now()}")

        
        if otp_obj.otp == int(otp):
            try:
                otp_obj.verified = True
                otp_obj.save()
                return JsonResponse({'message': 'otp_verified successfully'})
            except Exception as e:
                print(f"An error occurred during OTP verification: {e}")
                return JsonResponse({'error': 'Error during OTP verification'}, status=500)
        else:
            print("Incorrect otp")
            return JsonResponse({'error': 'Incorrect otp'}, status=400)

        
    except AuthenticationFailed as e:
        logger.error(f'Authentication failed: {e}', exc_info=True)
        return JsonResponse({'error': 'Authentication failed'}, status=401)
    except Http404:
        logger.error('Otp not found', exc_info=True)
        return JsonResponse({'error': 'Otp not found'}, status=404)
    except Exception as e:
        logger.error(f'Error in verify_otp: {e}', exc_info=True)
        return JsonResponse({'error': 'Internal Server Error'}, status=500)


@csrf_exempt
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def create_account(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))

            fullname = data.get('fullname')
            email = data.get('email')
            phone = data.get('phone')
            password = data.get('password')
            

            print(f"Received data - Email: {email}, Phone: {phone}, Password: {password}, Fullname: {fullname}")

            if email and phone and password and fullname:
                print(f"Trying to find Otp for phone: {phone}")
                User.objects.create(email=email, phone=phone, fullname=fullname, password=password,id=email)   
                return JsonResponse({"message": "account created successfully"})
            else:
                error_message = "Invalid data provided. "
                if not email:
                    error_message += "Email is required. "
                if not phone:
                    error_message += "Phone is required. "
                if not password:
                    error_message += "Password is required. "
                if not fullname:
                    error_message += "Fullname is required. "

                print(f"Error message: {error_message.strip()}")

                return JsonResponse({"error": error_message.strip()}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format in the request body"}, status=400)

        except Exception as e:
            print(f"Error: {str(e)}")
            return JsonResponse({"error": "An error occurred while processing the request"}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt 
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def login(request):
    email = request.data.get('email')
    phone = request.data.get('phone')
    password = request.data.get('password')

    if email:
        user = User.objects.filter(email=email).first()
        
        password1 = user.password if user else None
        print(password1) 
    elif phone:
        user = User.objects.filter(phone=phone).first()
        password1 = user.password if user else None
    else:
        return JsonResponse({'error': 'data missing'}, status=400)

    if user :
        if password == password1:
            return token_response(user)
        else :
            return JsonResponse({'response':'mdpincorrecte'})
    else:
        return JsonResponse({'error': 'incorrect password'}, status=400)
    

@csrf_exempt 
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def login_pour_medecin(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if email:
        user = Medecin.objects.filter(email=email).first()
        
        password1 = user.password if user else None
    
    else:
        return JsonResponse({'error': 'data missing'}, status=400)

    if user :
        if password == password1:
            return token_response_doctor(user)
        else :
            return JsonResponse({'response':'mdpincorrecte'})
    else:
        return JsonResponse({'error': 'incorrect password'}, status=400)
    
    
@csrf_exempt 
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def login_pour_agent(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if email:
        user = Agent.objects.filter(email=email).first()
        print(user.password)
        password1 = user.password if user else None
    
    else:
        return JsonResponse({'error': 'data missing'}, status=400)

    if user :
        if password == password1:
            return token_response_Agent(user)
        else :
            return JsonResponse({'response':'mdpincorrecte'})
    else:
        return JsonResponse({'error': 'incorrect password'}, status=400)
     
    
    
    
@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def password_reset_email(request):
    if request.method == 'GET':
        return render(request, 'emails/reset-password.html')
    
    elif request.method == 'POST':
        email = request.data.get('email')
        if not email:
            return JsonResponse({'error': 'params_missing'}, status=400)

        user = User.objects.filter(email=email).first()
        
        send_password_reset_email(user)
        return JsonResponse({'message': 'password_reset_email_sent'}, status=200)
    
    return JsonResponse({'error': 'Method Not Allowed'}, status=405)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def password_reset_form(request, email, token):
    token_instance = PasswordResetToken.objects.filter(user__email=email, token=token).first()
    link_expired = loader.get_template('pages/link-expired.html').render()

    if token_instance:
        if datetime.datetime.utcnow() < token_instance.validity.replace(tzinfo=None):
            return render(request, 'pages/new-password-form.html', {
                'email': email,
                'token': token,
                'base_url': TEMPLATES_BASE_URL,
            })
        else:
            token_instance.delete()
            return HttpResponse(link_expired)

    else:
        return HttpResponse(link_expired)
        
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def password_reset_confirm(request, email, token):
    email = request.data.get('email')
    token = request.data.get('token')
    password1 = request.data.get('password1')
    password2 = request.data.get('password2')
    print(password1)
    
    token_instance = PasswordResetToken.objects.filter(user__email=email, token=token).first()
    link_expired = get_template('pages/link-expired.html').render()
    if token_instance:
        if datetime.datetime.utcnow() < token_instance.validity.replace(tzinfo=None):
            if len(password1) < 8:
                return render(request, 'pages/new-password-form.html', {
                    'email': email,
                    'token': token,
                    'base_url': TEMPLATES_BASE_URL,
                    'error': 'Password length must be at least 8'
                })

            if password1 == password2:
                link_success = get_template('pages/password-updated.html').render()
                user = token_instance.user
                User.objects.filter(email=user.email).update(password=password1)
                token_instance.delete()
                Token.objects.filter(user=user).delete()
                return HttpResponse(link_success)
            else:
                return render(request, 'pages/new-password-form.html', {
                    'email': email,
                    'token': token,
                    'base_url': TEMPLATES_BASE_URL,
                    'error': 'Password 1 must be equal to password 2'
                })
        else:
            token_instance.delete()
            return HttpResponse(link_expired)
    else:
        return HttpResponse(link_expired)
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def password_updated(request) : 
    return render(request,'pages/password-updated.html')

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@login_required
def userData(request):
    print("Vue userData atteinte")
    if request.user.is_authenticated:
        user = request.user
        print("houni : ",user)
        
        data = {
            'email': user.email,
            'fullname': user.fullname,
            'phone': user.phone,
        }

        return JsonResponse(data)
    else:
        return JsonResponse({'detail': 'User not authenticated'}, status=401)


logger = logging.getLogger(__name__)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def logout_patient(request, token):
    logger.debug("Request data: %s", request.data)
    token_value = request.data.get('token')  # Use request.data to get POST data in DRF

    if not token_value:
        logger.error("Token not provided")
        return Response({"error": "Token not provided"}, status=400)

    try:
        token_obj = Token.objects.get(token=token_value)
        token_obj.delete()
        logger.info("Token successfully deleted")
        return HttpResponseRedirect('//')
    except Token.DoesNotExist:
        logger.error("Invalid token: %s", token_value)
        return Response({"error": "Invalid token"}, status=400)
    
    

@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def logout_medecin(request,token):
    logger.debug("Request data: %s", request.data)
    token_value = request.data.get('token')  # Use request.data to get POST data in DRF

    if not token_value:
        logger.error("Token not provided")
        return Response({"error": "Token not provided"}, status=400)

    try:
        token_obj = TokenForDoctor.objects.get(token=token_value)
        token_obj.delete()
        logger.info("Token successfully deleted")
        return HttpResponseRedirect('//')
    except TokenForDoctor.DoesNotExist:
        logger.error("Invalid token: %s", token_value)
        return Response({"error": "Invalid token"}, status=400)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def logout_Agent(request,token):
    logger.debug("Request data: %s", request.data)
    token_value = request.data.get('token')  # Use request.data to get POST data in DRF

    if not token_value:
        logger.error("Token not provided")
        return Response({"error": "Token not provided"}, status=400)

    try:
        token_obj = TokenForAgent.objects.get(token=token_value)
        token_obj.delete()
        logger.info("Token successfully deleted")
        return HttpResponseRedirect('//')
    except TokenForAgent.DoesNotExist:
        logger.error("Invalid token: %s", token_value)
        return Response({"error": "Invalid token"}, status=400)
