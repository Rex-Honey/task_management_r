from django.db import models
from authentication.models import CustomUser

class Task_data(models.Model):
    task_title=models.CharField(max_length=100)
    task_description=models.TextField()
    status=models.CharField(max_length=20,default="ToDo")
    assignee=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='assign_task',null=True)
    created_by=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='create_task',null=True)
    modified_by=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='modify_task',null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)