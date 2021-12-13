from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from .serializers import RegistrationSerializer
from user import models

@api_view(['POST',])
def logoutView(request):
    
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

@api_view(['POST',])
def registrationView(request):

    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)

        data = {}

        if serializer.is_valid():
            account = serializer.save()

            data['response'] = "Registration Successful"
            data['username'] = account.username
            data['email'] = account.email
            data['token'] = Token.objects.get(user=account).key
        else:
            data = serializer.errors
            
        return Response(data, status=status.HTTP_201_CREATED)

