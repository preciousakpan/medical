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
        token['name'] = user.username
        token['is_admin'] = user.is_staff

        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff