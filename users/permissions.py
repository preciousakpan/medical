from rest_framework.permissions import BasePermission

class IsTokenOwner(BasePermission):
    def has_permission(self, request, view):
        user_from_token = request.user
        username_from_request = request.data.get('name')
        return user_from_token.username == username_from_request
