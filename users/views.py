from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from .services import UserService
from django.core.exceptions import ValidationError
from medical.response_handler import ResponseHandler
from django.contrib.auth.models import User
from django.http import JsonResponse

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
                return JsonResponse(ResponseHandler.error(user), status=400)
            else:
                return JsonResponse(ResponseHandler.success('User created successfully'), status=201)
        except ValidationError as e:
            return JsonResponse(ResponseHandler.error(str(e)), status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users_view(request):
    if request.method == 'GET':
        try:
            users_json = UserService.get_all_users()
            return JsonResponse(ResponseHandler.success(users_json), status=200)
        except Exception as e:
            return JsonResponse(ResponseHandler.error(str(e)), status=400)
        
@api_view(['POST'])
def generate_reset_token_view(request):
    if request.method == 'POST':
        try:
            name = request.data.get('name')
            if request.user.username != str(name):
                return JsonResponse(ResponseHandler.error("Unauthorized access"), status=403)

            user = User.objects.get(username=name)
            token = UserService.generate_reset_token(user)
            return JsonResponse(ResponseHandler.success(token), status=200)
        except User.DoesNotExist:
            return JsonResponse(ResponseHandler.error('User not found'), status=404)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reset_password_view(request):
    if request.method == 'POST':
        token = request.data.get('token')
        new_password = request.data.get('new_password')
        
        success, message = UserService.reset_password(token, new_password, request.user.id)
        if success:
            return JsonResponse(ResponseHandler.success(message), status=200)
        else:
            return JsonResponse(ResponseHandler.error(message), status=400)
        
@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        username = request.data.get('name')
        password = request.data.get('password')
        
        success, user, token = UserService.login(username, password)
        
        if success:
            return JsonResponse(ResponseHandler.success({
                'message': 'Login successful',
                'token': token
            }), status=200)        
        else:
            return JsonResponse(ResponseHandler.error('Login failed, please check credentials'), status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users_view(request):
    if request.method == 'GET':
        try:
            users_json = UserService.get_all_users()
            return JsonResponse(ResponseHandler.success(users_json), status=200)
        except Exception as e:
            return JsonResponse(ResponseHandler.error(str(e)), status=400)