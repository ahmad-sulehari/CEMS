from rest_framework import serializers
from .models import *


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = [
            'f_name', 'l_name', 'date_of_birth', 'gender', 'email', 'password', 'degree', 'section', 'session',
            'student_id_number', 'student_id', 'phone_number',
        ]
        extra_kwargs = {'password': {'write_only': True}}

    # def validate_email(self, value):
    #     if '@pucit.edu.pk' not in value:
    #         raise serializers.ValidationError("must use university email only")
    #     return value


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = [
           'id', 'title', 'description', 'time_limit', 'team_size'
        ]


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
           'id', 'title', 'start_date', 'end_date', 'location', 'description'
        ]


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'event_id', 'game_id', 'user_id', 'payment_type', 'amount', 'status', 'verification_date', 'submission_date'
        ]
        extra_kwargs = {'submission_date': {'read_only': True},
                        'verification_date': {'read_only': True},
                        'status': {'read_only': True},
                        }


class UpdateDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = [
            'f_name', 'l_name', 'phone_number',
        ]
        extra_kwargs = {'password': {'write_only': True}}

    # def validate_email(self, value):
    #     if '@pucit.edu.pk' not in value:
    #         raise serializers.ValidationError("must use university email only")
    #     return value


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = MyUser
        fields = ['token']


class LoginDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = [
            'email', 'password',
        ]

'''
class SignupDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = [
            'f_name', 'l_name', 'age', 'gender', 'email', 'password', 'degree', 'section', 'session',
            'student_id_number', 'username', 'phone_number'
        ]
'''