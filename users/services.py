from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.hashers import make_password
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth import authenticate

class UserService:
    @staticmethod
    def create_user(name, email, password, is_admin):
        hashed_password = make_password(password)
        try:
            existing_user = User.objects.filter(email=email).exists()
            existing_name = User.objects.filter(username=name).exists()
            
            if existing_user:
                raise ValidationError("User with this email already exists.")
            
            if existing_name:
                raise ValidationError("User with this name already exists.")


            user = User.objects.create(username=name, email=email, password=hashed_password, is_staff=is_admin)
            return user
        except ValidationError as e:
            return str(e)
        
    @staticmethod
    def get_all_users():
        users = User.objects.all()
        users_data = [
            {
                'id': user.id,
                'name': user.username,
                'email': user.email,
                'is_admin': user.is_staff,
                'date_joined': user.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
            }
            for user in users
        ]
        
        return users_data

    @staticmethod
    def generate_reset_token(user):
        return default_token_generator.make_token(user)


# TODO: Fix reset password
    @staticmethod
    def reset_password(token, new_password, user_id):
        try:
            uid = str(urlsafe_base64_decode(token))
            user = User.objects.get(pk=user_id)
            if default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                return True, "Password Reset Successful"
            else:
                return False, "Invalid Token"
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return False, "User Not Found"

    @staticmethod
    def login(name, password):
        user = authenticate(username=name, password=password)
        if user is not None:
            return True, user
        else:
            return False, None
