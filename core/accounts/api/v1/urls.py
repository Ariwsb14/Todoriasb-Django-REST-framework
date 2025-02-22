from django.urls import path , include
from . import views
from  django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView ,TokenRefreshView , TokenVerifyView


app_name = 'api-v1'
urlpatterns = [
    #registration
    path('registration/', views.RegistrationAPIView.as_view(), name='registration'),
    # login and logout based on token
    path('token/login/',views.CustomObtainAuthToken.as_view(),name='token-login'),
    path('token/logout',views.CustomDiscardAuthToken.as_view(),name ='token-logout'),
    # login based on Jason Web Token
    path('jwt/create/',views.CustomTokenObtainPairView.as_view(), name='jwt-create'),
    path('jwt/refresh/',TokenRefreshView.as_view(),name='jwt-refresh'),
    path('jwt/verify/',TokenVerifyView.as_view(),name='jwt-verify'),
    # change password
    path('change-password/',views.ChangePasswordAPIView.as_view(),name='change-password'),
    # user profile
    path('profile/', views.ProfileAPIView.as_view(),name='profile'),
    #user activation
    path('activation/confirm/<str:token>' ,views.ActivationEmailAPIView.as_view(), name='email-activation'),
    path('test-email', views.TestEmailSend.as_view(),name='test'),
    path('activation/resend/',views.ActivationResendAPIView.as_view(),name='activation-resend')
]