from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):
    """"Model class for user"""
    date_of_birth = models.DateField(null=False)
    email = models.EmailField(unique=True, null=False)
    phone_number = models.IntegerField(null=False,unique=True)
    street = models.CharField(null=False, max_length=100)
    zip_code = models.CharField(null=False, max_length=10)
    city = models.CharField(null=False, max_length=100)
    state = models.CharField(null=False, max_length=100)
    country = models.CharField(null=False, max_length=100)
    password = models.CharField(max_length=10)

