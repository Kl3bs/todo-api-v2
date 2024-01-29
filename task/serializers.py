from rest_framework import serializers
from task.models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'user', 'created_at']
        extra_kwargs = {'id': {'required': True},
                        'title': {'required': True},
                        'description': {'required': True},
                        'user': {'required': True},
                                }