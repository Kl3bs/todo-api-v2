from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from task.models import Task
from task.serializers import TaskSerializer

from rest_framework.decorators import action
from rest_framework import viewsets


class TaskView(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    #Get all tasks
    @action(detail=False, methods=['GET'])

    def list_all(self,request):
        tasks = self.get_queryset()
        serializer = TaskSerializer(tasks, many=True)
        return Response({"tasks":serializer.data})
    
    #Get task by id
    @action(detail=True, methods=['GET'])
    def details(self, request, pk=None):
        task = Task.objects.get(id=pk)
    
        if task:
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    #Create task
    def post(self,request):
        serializer = TaskSerializer(data = request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
    #Delete task    
    def delete(self,request, id):
       task = Task.objects.get(id=id)
       if task:
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
       else:
        return Response(status=status.HTTP_404_NOT_FOUND)
       

    #Edit task
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