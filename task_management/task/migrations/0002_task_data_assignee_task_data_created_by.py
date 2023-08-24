# Generated by Django 4.2.4 on 2023-08-24 03:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task_data',
            name='assignee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assign_task', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='task_data',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='create_task', to=settings.AUTH_USER_MODEL),
        ),
    ]