from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User

class IsTokenOwner(BasePermission):
    def has_permission(self, request, view):
        user_from_token = request.user
        username_from_request = request.data.get('name')
        return user_from_token.username == username_from_request

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user:User):
        token = super().get_token(user)
        token['role'] = user.is_staff

        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    pass