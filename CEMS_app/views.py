from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions, status, authentication
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from .serializers import *
from .models import *
from drf_multiple_model.views import ObjectMultipleModelAPIView


class APIOverView(APIView):

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        api_urls = {
            'Login': 'login/',
            'Signup': 'signup/'
        }
        return Response(api_urls)


class LoginView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginDataSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(request.data)
        email = serializer.data['email']
        password = serializer.data['password']
        if Person.objects.filter(email=email).exists() and Person.objects.filter(password=password).exists():
            return Response(status=status.HTTP_200_OK)
        else:
            content = {'error': "email or password not correct"}
            return Response(content, status=status.HTTP_204_NO_CONTENT)


class UserDataView(ObjectMultipleModelAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication]

    querylist = [
        {'queryset': Person.objects.all(), 'serializer_class': LoginDataSerializer},
        {'queryset': Category.objects.all(), 'serializer_class': LoginDataSerializer},
    ]


class SignUpView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = SignupDataSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid(raise_exception=True):  # Also checks it data already exists
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


'''
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
'''