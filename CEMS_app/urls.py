from django.urls import path, re_path
from . import views

# app_name = ''

urlpatterns = [

    path('', views.APIOverView.as_view(), name='api-overview'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('email-verify/', views.VerifyEmail.as_view(), name='email-verify'),
    path('logout/blacklist/', views.BlackListTokenView.as_view(), name='blacklist'),
    path('update-profile/<int:pk>/', views.UpdateProfile.as_view(), name='update-profile'),
    path('games/<int:event_id>/', views.RetrieveGames.as_view(), name='game-list'),
    path('event-details/', views.EventDetails.as_view(), name='event-details'),
    re_path(r'^payment-request/$', views.PaymentRequest.as_view(), name='payment-request'),
    re_path(r'^payment-request/(?P<event_id>\w+)/(?P<user_id>\w+)/$', views.PaymentList.as_view(), name='payment-list'),

]
