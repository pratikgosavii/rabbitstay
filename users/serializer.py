
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import *

class user_serializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = [
            'id',
            'mobile',
            'email',
            'firebase_uid',
            'first_name',
            'last_name',
            'is_customer',
            'is_doctor',
            'is_daycare',
            'is_service_provider',
        ]
        read_only_fields = ['id', 'firebase_uid']