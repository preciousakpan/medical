from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.hashers import make_password

class AuthService:
    @staticmethod
    def create_user(name, email, password):
        hashed_password = make_password(password)
        user = User.objects.create(name=name, email=email, password=hashed_password)
        return user

    @staticmethod
    def generate_reset_token(user):
        return default_token_generator.make_token(user)

    @staticmethod
    def reset_password(token, new_password):
        try:
            uid = force_text(urlsafe_base64_decode(token))
            user = User.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                return True, "Password Reset Successful"
            else:
                return False, "Invalid Token"
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return False, "User Not Found"
