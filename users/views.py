from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from .services import UserService
from django.core.exceptions import ValidationError
from medical.response_handler import ResponseHandler
from django.contrib.auth.models import User
from .permissions import IsTokenOwner

@api_view(['POST'])
def create_user_view(request):
    if request.method == 'POST':
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')
        is_admin = request.data.get('is_admin')
        
        try:
            user = UserService.create_user(name, email, password, is_admin)
            if isinstance(user, str):
                return ResponseHandler.error(user)
            else:
                return ResponseHandler.success('User created successfully')
        except ValidationError as e:
            return ResponseHandler.error(str(e))

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users_view(request):
    if request.method == 'GET':
        try:
            users_json = UserService.get_all_users()
            return ResponseHandler.success(users_json)
        except Exception as e:
            return ResponseHandler.error(str(e))
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_reset_token_view(request):
    if request.method == 'POST':
        try:
            email = request.data.get('email')
            user = User.objects.get(email=email)
            token = UserService.generate_reset_token(user)
            return ResponseHandler.success(token)
        except User.DoesNotExist:
            return ResponseHandler.error('User not found', status_code=404)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reset_password_view(request):
    if request.method == 'POST':
        token = request.data.get('token')
        new_password = request.data.get('new_password')
        
        success, message = UserService.reset_password(token, new_password)
        if success:
            return ResponseHandler.success(message)
        else:
            return ResponseHandler.error(message)
        
@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        username = request.data.get('name')
        password = request.data.get('password')
        
        success, user = UserService.login(username, password)
        
        if success:
            return ResponseHandler.success('Login successful')
        else:
            return ResponseHandler.error('Login failed, please check credentials')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users_view(request):
    if request.method == 'GET':
        try:
            users_json = UserService.get_all_users()
            return ResponseHandler.success(users_json)
        except Exception as e:
            return ResponseHandler.error(str(e))