from django.shortcuts import render
# from django.contrib.auth.models import User
from rest_framework import viewsets
# from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import permissions, status, authentication, views
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from .serializers import *
from .models import *
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from dotenv import load_dotenv
import os
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from . import tokens
from rest_framework.parsers import FileUploadParser
from django.utils.timezone import now
from drf_multiple_model.views import ObjectMultipleModelAPIView

load_dotenv()


class APIOverView(APIView):

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        api_urls = {
            'Login': 'login/',
            'Signup': 'signup/',
            'Retrieve Game List': 'games/<int:event_id>/',
            'Update user profile': 'update-profile/<int:pk>/',
            'Event Details': 'event-details/',
        }
        return Response(api_urls)


class LoginView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginDataSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(request.data)
        email = serializer.data['email']
        password = serializer.data['password']
        if MyUser.objects.filter(email=email).exists():
            user = MyUser.objects.get(email=email)
            if not check_password(password, user.password):
                return Response({'error': 'Password not correct'}, status.HTTP_401_UNAUTHORIZED)
            if not user.is_verified:
                return Response({'error': 'Email not verified.'}, status=status.HTTP_401_UNAUTHORIZED)
            if not user.is_active:
                return Response({'error': 'Account disabled. Contact the admin'}, status=status.HTTP_401_UNAUTHORIZED)
            data = {
                'user_id': user.id,
                'email': user.email,
                'username': user.student_id,
                'full_name': user.get_full_name(),
                'tokens': user.get_tokens(),
            }
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            content = {'error': "email not correct"}
            return Response(content, status=status.HTTP_204_NO_CONTENT)


class UserAvatar(APIView):
    parser_classes = [FileUploadParser]
    permission_classes = [permissions.AllowAny]

    def put(self, request, filename):
        file_obj = request.data['file']


'''
class UserDataView(ObjectMultipleModelAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication]

    querylist = [
        {'queryset': Person.objects.all(), 'serializer_class': LoginDataSerializer},
        {'queryset': Category.objects.all(), 'serializer_class': LoginDataSerializer},
    ]

'''


class SignUpView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = SignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid(raise_exception=True):  # Also checks it data already exists
            passwd = make_password(serializer.validated_data['password'])
            serializer.validated_data['password'] = passwd
            serializer.save()
            user = MyUser.objects.get(email=request.data['email'])

            # token = RefreshToken.for_user(user=user).access_token
            token = tokens.generate_access_token(user=user)

            current_site = get_current_site(request).domain
            relative_link = reverse('email-verify')

            absolute_url = 'http://' + current_site + relative_link + '?token=' + str(token)
            email_body = 'Hi ' + user.student_id + '\nUser link below to verify your email\n' + absolute_url

            data = {
                'email_subject': 'Verify your Email for Sports Society',
                'email_body': email_body,
                'to_email': user.email,
                }
            Util.send_email(data=data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description='verification token', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            SECRET_KEY = os.getenv('SECRET_KEY')
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            user = MyUser.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'activation link expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({'error': 'invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class BlackListTokenView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UpdateProfile(generics.UpdateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UpdateDataSerializer
    queryset = MyUser.objects.all()


class RetrieveGames(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = GameSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        event_id = self.kwargs['event_id']
        queryset = self.model.objects.filter(is_active=True, event_id=event_id)
        return queryset


class EventDetails(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = EventSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.filter(is_active=True)


class PaymentList(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = PaymentSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        event_id = self.kwargs['event_id']
        user_id = self.kwargs['user_id']
        queryset = self.model.objects.filter(event_id=event_id, user_id=user_id)
        return queryset


class PaymentRequest(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = PaymentSerializer


