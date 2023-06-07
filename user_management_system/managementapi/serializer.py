import six
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
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
    username_or_email = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=30)

    def validate(self, attrs):
        username_or_email = attrs.get('username_or_email')
        password = attrs.get('password')
        # username_or_email = attrs.get('username_or_email')
        if username_or_email and password:
            user = authenticate(request=self.context.get('request'), username=username_or_email, password=password)
            if not user:
                try:
                    user = CustomUser.objects.get(email=username_or_email)
                    user = authenticate(request=self.context.get('request'), username=user.username, password=password)
                except:
                    raise serializers.ValidationError('Unable to do login provide valid credentials')
        else:
            raise serializers.ValidationError("Invalid credentials")
        attrs['user'] = user
        return attrs


class UserTokenGenerator(PasswordResetTokenGenerator):
    """This class is used for generate token"""

    def _make_hash_value(self, user, timestamp):
        return six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)


Generated_Token = UserTokenGenerator()


class ChangePasswordSerilizer(serializers.Serializer):
    """This class is used for reset password and provides two fields new_password and confirm_password"""
    model = CustomUser
    new_password = serializers.CharField(max_length=20)
    confirm_password = serializers.CharField(max_length=20)

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        if new_password != confirm_password:
            raise serializers.ValidationError("You had entered incorrect password")

        return attrs
