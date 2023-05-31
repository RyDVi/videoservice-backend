from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend


class EmailOrUsernameModelBackend(ModelBackend):
    """
    This is a ModelBacked that allows authentication
    with either a username or an email address.

    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if "@" in username:
            kwargs = {**kwargs, "email": username}
        else:
            kwargs = {**kwargs, "username": username}
        try:
            user = get_user_model().objects.get(**kwargs)
            if user.check_password(password):
                return user if self.user_can_authenticate(user) else None
        except User.DoesNotExist:
            return None

    def get_user(self, username):
        try:
            user = get_user_model().objects.get(pk=username)
        except get_user_model().DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None
