from rest_framework import serializers
from .models import *


class LoginDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = [
            'email', 'password',
        ]


class SignupDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = [
            'f_name', 'l_name', 'age', 'gender', 'email', 'password', 'degree', 'section', 'session',
            'student_id_number', 'username', 'phone_number'
        ]
