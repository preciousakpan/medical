from rest_framework.decorators import api_view
from .services import AuthService
from .response_handler import ResponseHandler

@api_view(['POST'])
def create_user_view(request):
    if request.method == 'POST':
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')
        
        user = AuthService.create_user(name, email, password)
        if user:
            return ResponseHandler.success('User created successfully')
        else:
            return ResponseHandler.error('Failed to create user')

@api_view(['POST'])
def reset_password_view(request):
    if request.method == 'POST':
        token = request.data.get('token')
        new_password = request.data.get('new_password')
        
        success, message = AuthService.reset_password(token, new_password)
        if success:
            return ResponseHandler.success(message)
        else:
            return ResponseHandler.error(message)
