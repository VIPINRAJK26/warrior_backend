from django.contrib.auth.backends import BaseBackend
from django.db import models
from warrior_app.models import User

class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(
                models.Q(email__iexact=username) | 
                models.Q(username__iexact=username)
            )
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
