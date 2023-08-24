from django.contrib import admin
from authentication.models import *
from django.contrib.auth.admin import UserAdmin

class MyUserAdmin(UserAdmin):
    model=CustomUser
    list_display=['id','username','first_name','last_name','mobile','user_type','is_superuser']
admin.site.register(CustomUser,MyUserAdmin)