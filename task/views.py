from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from task.models import Task
from task.serializers import TaskSerializer

from rest_framework.decorators import action
from rest_framework import viewsets


from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes

 

class TaskView(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    # Adicionando autenticação e permissão para todas as ações
    @authentication_classes([TokenAuthentication, SessionAuthentication])
    @permission_classes([IsAuthenticated])
    # Get all tasks
    @action(detail=False, methods=['GET'])
    def list_all(self, request):
        user = self.request.user
        tasks = Task.objects.filter(user=user)
        #serializer = TaskSerializer(tasks, many=True)
 
        return tasks

    # Get task by id
    @action(detail=True, methods=['GET'])
    def details(self, request, pk=None):
        task = Task.objects.get(id=pk)

        if task:
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def perform_create(self, serializer):
        # Set the user before saving the task
        serializer.save(user=self.request.user)

    # Create task
    @authentication_classes([TokenAuthentication, SessionAuthentication])
    @permission_classes([IsAuthenticated])
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            # Call perform_create to set the user before saving
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # Delete task
    @authentication_classes([TokenAuthentication, SessionAuthentication])
    @permission_classes([IsAuthenticated])
    def delete(self, request, id):
        task = Task.objects.get(id=id)
        if task:
            task.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # Edit task
    @authentication_classes([TokenAuthentication, SessionAuthentication])
    @permission_classes([IsAuthenticated])
    def patch(self, request, id):
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
