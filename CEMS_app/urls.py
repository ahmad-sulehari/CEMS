from django.urls import path
from . import views

urlpatterns = [
    path('', views.APIOverView.as_view(), name='api-overview'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
]
