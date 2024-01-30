from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from authentication.serializers import UserSerializer
from task.models import Task
from task.serializers import TaskSerializer

from rest_framework.decorators import action
from rest_framework import viewsets
from django.contrib.auth.models import User


from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes

 



# Adicionando autenticação e permissão para todas as ações
# Get all tasks
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def list_all(request):
    tasks = Task.objects.filter(user=request.user)
    serializer = TaskSerializer(tasks, many=True)
 
    return Response({"tasks":serializer.data}, status=status.HTTP_200_OK)

# Get task by id
@api_view(['GET'])
def details(self, request, pk=None):
    task = Task.objects.get(id=pk)

    if task:
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

def perform_create(request, serializer):
    # Set the user before saving the task
    serializer.save(user=request.user)


# Create 
@api_view(['POST'])    
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def create(request):
    serializer = TaskSerializer(data=request.data)
     
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Delete task
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def delete(request, id):
    task = Task.objects.get(id=id)
    if task:
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

# Edit task
@api_view(['PATCH'])
# @authentication_classes([TokenAuthentication, SessionAuthentication])
# @permission_classes([IsAuthenticated])
def edit(request, id):

    task = Task.objects.get(id=id)
    if task:
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
