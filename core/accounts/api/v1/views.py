from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import (RegistrationsSerializer , CustomAuthTokenSerializer, 
                          CustomTokenObtainPairSerializer ,ChangePasswordSerializer , 
                          ProfileAPISerializer , ActivationResendSerializer)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from accounts.models import User , Profile
from django.shortcuts import get_object_or_404
from mail_templated import EmailMessage
from ..utils import EmailThread
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from jwt.exceptions import ExpiredSignatureError , InvalidSignatureError
from django.conf import settings

# make your views here

'''
user registration view with email , password, password confirmations(password1)
'''
class RegistrationAPIView(generics.CreateAPIView):
    serializer_class = RegistrationsSerializer
    def post(self, request, *args, **kwargs):
        serializer = RegistrationsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'email': serializer.validated_data['email'],
            }
            user = get_object_or_404(User,email=serializer.validated_data['email'])
            token = self.get_tokens_for_user(user)
            email_obj = EmailMessage('email/activation.tpl', {'token':token}, 'admin@admin.com', to=[user.email])
            EmailThread(email_obj).start()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# generating token for each user ( for user verification)
    def get_tokens_for_user(self,user):
        refresh = RefreshToken.for_user(user)
    
        return str(refresh.access_token)

'''
Token based login and token generating
'''
class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
            }
        )

'''
token based logout and deleting the token of user
'''
class CustomDiscardAuthToken(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
'''
creating and login with Jason Web Token.
'''
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class=  CustomTokenObtainPairSerializer


class ChangePasswordAPIView(generics.GenericAPIView):
    serializer_class= ChangePasswordSerializer
    model = User
    permission_classes = [IsAuthenticated]
    def get_object(self):
        obj = self.request.user
        return obj
    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get('old_password')):
                return Response({'old_password':['wrong password']}, status = status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get('new_password'))
            self.object.save()
            return Response({'details': 'password change successfully'} , status = status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileAPISerializer
    queryset = Profile.objects.all()
    def get_object(self):
        query_set = self.get_queryset()
        obj = get_object_or_404(query_set,user=self.request.user)
        return obj

class TestEmailSend(generics.GenericAPIView):
    
    def get(self,request,*args,**kwargs):
        self.email = 'Ariasb1385@gmail.com'
        user = get_object_or_404(User,email=self.email)
        token = self.get_tokens_for_user(user)
        email_obj = EmailMessage('email/hello.tpl', {'token':token}, 'admin@admin.com', to=[self.email])
        EmailThread(email_obj).start()
        return Response('email sent')
    
    def get_tokens_for_user(self,user):
        refresh = RefreshToken.for_user(user)

        return str(refresh.access_token)
    
class ActivationEmailAPIView(APIView):
    def get(self,request,token,*args,**kwargs):
        try:
            token = jwt.decode(token , settings.SECRET_KEY, algorithms=["HS256"])
            user_id = token.get('user_id')
        except InvalidSignatureError:
            return Response({'details':'your jwt token is invalid'})
        except ExpiredSignatureError:
            return Response({'details':'yor token has been expired'})
        user_obj = User.objects.get(pk = user_id)
        if user_obj.is_verified == True:
            return Response({'details': 'yor account has already been verified'})
        user_obj.is_verified = True
        user_obj.save()
        return Response({'details':'your account have been successfully verified'})

class ActivationResendAPIView(generics.GenericAPIView):
    serializer_class = ActivationResendSerializer

    def post(self, request,*args,**kwargs):
        serializer = ActivationResendSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data['user']
        token = self.get_tokens_for_user(user_obj)
        email_obj = EmailMessage('email/activation.tpl', {'token':token}, 'admin@admin.com', to=[user_obj.email])
        EmailThread(email_obj).start()
        return Response({'details':'user activation send successfully'} , status=status.HTTP_200_OK)

    def get_tokens_for_user(self,user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)