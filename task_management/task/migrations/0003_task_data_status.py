# Generated by Django 4.2.4 on 2023-08-24 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_task_data_assignee_task_data_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='task_data',
            name='status',
            field=models.CharField(default='ToDo', max_length=20),
        ),
    ]