# Generated by Django 4.2.9 on 2024-01-26 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_remove_task_date_time_remove_task_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='title',
            field=models.CharField(default='', max_length=200),
        ),
    ]