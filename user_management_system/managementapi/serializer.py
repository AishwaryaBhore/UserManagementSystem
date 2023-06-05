import six
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import serializers
from .models import CustomUser


class CustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class CustomSerializerForUpdate(serializers.ModelSerializer):
    """"serializer class for post ,retrieve ,delete"""

    class Meta:
        model = CustomUser
        exclude = ['username', 'email', 'password']


class LoginSerializer(serializers.Serializer):
    """"Created fields for login API"""
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=30)


class UserTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)


Generated_Token = UserTokenGenerator()


class ChangePasswordSerilizer(serializers.Serializer):
    model = CustomUser

    new_password = serializers.CharField(max_length=20)
    confirm_password = serializers.CharField(max_length=20)

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        if new_password != confirm_password:
            raise serializers.ValidationError("password not match")

        return  attrs