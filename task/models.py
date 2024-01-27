from django.db import models

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=200, default='')
    description = models.TextField(default='');
    # duration = models.IntegerField();
    # date_time = models.DateTimeField();
    # place = models.CharField(max_length=200);
    # status = models.BooleanField();
    def __str__(self):
        return self.title + 'Funcionou'