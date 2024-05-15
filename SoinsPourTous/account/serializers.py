from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import  User
from .models import Service,Specialite
import base64
from .models import Grade, Groupe
from .models import Medecin

class MedecinSerializer(serializers.ModelSerializer):
    gouvernorat_name = serializers.CharField(source='gouvernorat.options', read_only=True)
    nationalite_name = serializers.CharField(source='nationalite.nationalite', read_only=True)
    groupe_name = serializers.CharField(source='groupe.groupe', read_only=True)
    grade_name = serializers.CharField(source='grade.grade', read_only=True)
    specialite_name = serializers.CharField(source='sepcialite.specialite', read_only=True)
    service_name = serializers.CharField(source='service.service', read_only=True)
    hopitale_name = serializers.CharField(source='hopitale.nom', read_only=True)
    image_base64 = serializers.SerializerMethodField()

    class Meta:
        model = Medecin
        fields = [
            'id', 'email', 'username', 'password', 'phone', 'fullname', 'date_nais',
            'gouvernorat_name', 'nationalite_name', 'groupe_name', 'grade_name',
            'specialite_name', 'service_name', 'hopitale_name', 'image_base64'
        ]
    def get_image_base64(self, obj):
        if obj.image and hasattr(obj.image, 'path'):
            try:
                with open(obj.image.path, "rb") as image_file:
                    return base64.b64encode(image_file.read()).decode('utf-8')
            except IOError:
                return None
        return None   
class User_Serializer(serializers.ModelSerializer):
    gouvernorat_name = serializers.CharField(source='gouvernorat.options', read_only=True)
    nationalite_name = serializers.CharField(source='nationalite.nationalite', read_only=True)
    
    image_base64 = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'password', 'phone', 'fullname', 'date_naiss',
            'gouvernorat_name', 'nationalite_name', 'image_base64'
        ]

    def get_image_base64(self, obj):
        if obj.image and hasattr(obj.image, 'path'):
            try:
                with open(obj.image.path, "rb") as image_file:
                    return base64.b64encode(image_file.read()).decode('utf-8')
            except IOError:
                return None
        return None

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'

class GroupeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groupe
        fields = '__all__' 

class SpecialiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialite
        fields = '__all__'

class UserSerializer(ModelSerializer) : 
    class Meta:
        model = User
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'