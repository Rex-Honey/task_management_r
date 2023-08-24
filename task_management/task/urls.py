from django.urls import path,re_path
from task import views

urlpatterns = [
    path('create_task/',views.Create_task,name='create_task'),
    path('update_task/',views.Update_task,name='update_task')
]