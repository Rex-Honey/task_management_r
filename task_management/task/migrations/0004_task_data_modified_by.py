# Generated by Django 4.2.4 on 2023-08-24 06:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('task', '0003_task_data_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='task_data',
            name='modified_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modify_task', to=settings.AUTH_USER_MODEL),
        ),
    ]
