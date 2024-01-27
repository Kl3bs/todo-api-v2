from task.views import TaskView

from django.urls import path, include
from rest_framework.routers import DefaultRouter

 
router = DefaultRouter()
router.register(r'task', TaskView)

urlpatterns = [
    path('', include(router.urls)),
]