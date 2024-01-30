from django.urls import re_path, path
from . import views

urlpatterns = [
    re_path('all', views.list_all),
    re_path('details', views.details),
    re_path('create', views.create),
    path('task/delete/<int:id>/', views.delete, name='delete') ,

    path('task/edit/<int:id>/', views.edit, name='edit') ,
]