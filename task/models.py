from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=200, default='')
    description = models.TextField(default='');
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True);
    # duration = models.IntegerField();
    # date_time = models.DateTimeField();
    # place = models.CharField(max_length=200);
    # status = models.BooleanField();
    def __str__(self):
        return self.title + 'Funcionou'