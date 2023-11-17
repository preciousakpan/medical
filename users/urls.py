from django.urls import path
from . import views

urlpatterns = [
    path('create-user/', views.create_user_view, name='create_user'),
    path('reset-password/', views.reset_password_view, name='reset_password'),
]
