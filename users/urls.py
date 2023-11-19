from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
from .permissions import CustomTokenObtainPairView


urlpatterns = [
    path('create-user/', views.create_user_view),
    path('get-users/', views.get_users_view),
    path('reset-password/', views.reset_password_view),
    path('login/', views.login_view),
    path('token/', CustomTokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]
