from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models


class CustomUser(AbstractUser):
    """"Model class for user"""
    first_name = models.CharField(max_length=40, null=False, blank=False)
    last_name = models.CharField(max_length=40, null=False, blank=False)
    date_of_birth = models.DateField(null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    phone_number = models.IntegerField(null=False, unique=True, blank=False)
    street = models.CharField(null=False, max_length=100, blank=False)
    zip_code = models.CharField(null=False, max_length=10, blank=True)
    city = models.CharField(null=False, max_length=100, blank=True)
    state = models.CharField(null=False, max_length=100, blank=True)
    country = models.CharField(null=False, max_length=100, blank=True)
    password = models.CharField(max_length=10, blank=True, validators=[MinLengthValidator(8)])
    user_permissions = None
    groups = None
