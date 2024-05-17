from rest_framework import serializers
from .models import Message, Notification
from django.contrib.auth.models import User

class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['id', 'user', 'value', 'date']

class NotificationSerializer(serializers.ModelSerializer):
    message = MessageSerializer()

    class Meta:
        model = Notification
        fields = ['id', 'value', 'seen', 'timestamp']