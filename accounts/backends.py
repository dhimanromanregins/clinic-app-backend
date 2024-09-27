# yourapp/backends.py

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

class PhoneNumberBackend(BaseBackend):
    def authenticate(self, request, phone_number=None):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(phone_number=phone_number)
            return user
        except UserModel.DoesNotExist:
            return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
