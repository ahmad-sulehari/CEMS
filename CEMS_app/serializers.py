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


class ProfileDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = [
            'f_name', 'l_name', 'date_of_birth', 'gender', 'email', 'student_id', 'phone_number', 'profile_image'
        ]
#        extra_kwargs = {'password': {'write_only': True}}

    # def validate_email(self, value):
    #     if '@pucit.edu.pk' not in value:
    #         raise serializers.ValidationError("must use university email only")
    #     return value


class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = [
            'profile_image'
        ]


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = [
           'id', 'title', 'description', 'time_limit', 'team_size', 'registration_fee'
        ]


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = [
            'url', 'title', 'description', 'image'
        ]


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
           'id', 'title', 'start_date', 'end_date', 'location', 'description', 'payment_account_number'
        ]
        extra_kwargs = {
            'payment_account_number': {'read_only': True},
        }


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'event_id', 'game_id', 'user_id', 'payment_type',
            'amount', 'status', 'verification_date', 'submission_date', 'tid',
        ]
        extra_kwargs = {'submission_date': {'read_only': True},
                        'verification_date': {'read_only': True},
                        'status': {'read_only': True},
                        }


class TeamGameEnrollment(serializers.ModelSerializer):
    class Meta:
        model = TeamEnrolment
        fields = '__all__'


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


class TeamDetails:
    def __init__(self, team_lead, team_name, team_size, team_members):
        self.team_lead = team_lead
        self.team_name = team_name
        self.team_size = team_size
        self.team_members = team_members


class TeamRegisterSerializer(serializers.Serializer):
    team_lead = serializers.IntegerField()
    team_name = serializers.CharField(max_length=60)
    team_size = serializers.IntegerField()
    team_members = serializers.ListField(
            child=serializers.CharField(max_length=10, validators=[MinLengthValidator(10)])
        )

    def update(self, instance, validated_data):
        instance.team_name = validated_data.get('team_name', instance.team_name)
        instance.team_members = validated_data.get('team_members', instance.team_members)
        return instance

    def create(self, validated_data):
        return TeamDetails(**validated_data)


'''
class SignupDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = [
            'f_name', 'l_name', 'age', 'gender', 'email', 'password', 'degree', 'section', 'session',
            'student_id_number', 'username', 'phone_number'
        ]
'''