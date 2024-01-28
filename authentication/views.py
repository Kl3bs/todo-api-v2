from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response    
from rest_framework.authtoken.models import Token

from authentication.serializers import UserSerializer

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated



@api_view(['POST'])
def login(request):

    #Return an object, or raise an Http404 exception if the object does not exist.
    user = get_object_or_404(User, username=request.data['username'])

    if not user.check_password(request.data['password']):
        return Response({"message": "Invalid Credentials"}, status=status.HTTP_404_NOT_FOUND)

    token, created = Token.objects.get_or_create(user=user)    
    serializer = UserSerializer(instance=user)

    return Response({"token":token.key, "user":serializer.data}, status=status.HTTP_201_CREATED)



@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)

    if (serializer.is_valid()):
        #Store the user in the database
        serializer.save()
        #Get the user from db
        user = User.objects.get(username=request.data['username'])
        #Hashing user passwort
        user.set_password(request.data['password'])
        user.save()
        #Creates user token
        token = Token.objects.create(user=user)
        return Response({"token":token.key, "user":serializer.data}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    
    return Response("Token is valid for {}".format(request.user.email), status=status.HTTP_200_OK)
