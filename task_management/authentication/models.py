from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    role_choices = (
        ('Admin', 'Admin'),
        ('Manager', 'Manager'),
        ('Developer', 'Developer')
    )

    user_type = models.CharField(
        max_length=50, choices=role_choices, default='Admin')
    mobile = models.CharField(max_length=10)