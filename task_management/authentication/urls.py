from django.urls import path
from authentication import views

urlpatterns = [
    path('create_user/',views.Create_user,name='create_user')
]