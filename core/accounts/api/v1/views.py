from rest_framework import generics
from .serializers import RegistrationsSerializer
from ..utils import EmailThread
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

#make your views here
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
