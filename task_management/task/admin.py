from django.contrib import admin
from task.models import *
from django.contrib.auth.admin import UserAdmin

class MyTaskAdmin(admin.ModelAdmin):
    model=Task_data
    list_display=['id','task_title','task_description','status','assignee','created_by','modified_by','created_at','modified_at']
admin.site.register(Task_data,MyTaskAdmin)