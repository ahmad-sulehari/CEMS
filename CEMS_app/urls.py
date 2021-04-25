from django.urls import path
from . import views

# app_name = ''

urlpatterns = [

    path('', views.APIOverView.as_view(), name='api-overview'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('email-verify/', views.VerifyEmail.as_view(), name='email-verify'),
    path('logout/blacklist/', views.BlackListTokenView.as_view(), name='blacklist'),

]
