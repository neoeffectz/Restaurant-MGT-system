from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from random import random
import uuid

# Create your models here.


#used the base user to replace the username with email as the authentication
class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, password, first_name='first_name', last_name='last_name', phone_number=random(), **extra_fields):

        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name =last_name, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)
        


# Created a custom user which can be used as foreign key for any other models, deleted the customer model

class CustomUser(AbstractUser):
    
    
    username = None
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField("First Name", max_length=30, null=False, blank=True)
    last_name = models.CharField("Last Name", max_length=30, null=True, blank=True)
    phone_number = models.CharField(
        "Phone Number", max_length=20, blank=True, null=False, unique=True, default=uuid.uuid1
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email