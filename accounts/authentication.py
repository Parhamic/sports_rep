from .models import User
from django.contrib.auth.forms import AuthenticationForm
from django import forms


class EmailAuthBackend():
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(raw_password=password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class CheckConfirmed(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.email_confirmed:
            raise forms.ValidationError(
                'Email is not confirmed',
                code='not_confirmed',
            )
