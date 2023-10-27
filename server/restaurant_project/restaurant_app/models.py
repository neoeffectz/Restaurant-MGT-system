from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _ 
from restaurant_project.settings import AUTH_USER_MODEL




class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, password, first_name, last_name, phone_number, role, **extra_fields):

        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name =last_name, phone_number=phone_number, role=role, **extra_fields)
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
        



class CustomUser(AbstractUser):
    class Roles(models.TextChoices):
        """define the user roles"""

        
        MANAGER = "MANAGER", "Manager"
        STAFF = "STAFF", "Staff"
        CLIENT = "CLIENT", "Client"
    
    username = None
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField("First Name", max_length=30, null=False)
    last_name = models.CharField("Last Name", max_length=30, null=True, blank=True)
    phone_number = models.CharField(
        "Phone Number", max_length=20, null=False, unique=True
    )
    role = models.CharField(max_length=50, default=Roles.CLIENT)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email










class Categories(models.Model):
    Categories = (
        ("Drinks", "Drinks"),
        ("Salads", "Salads"),
        ("Meat", "Meat"),
        ("Fruits", "Fruits"),
    )
    name = models.CharField(max_length=200, null=True, choices=Categories)
    image = models.ImageField(null=True, blank=True, upload_to="categories")
    
    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class MenuProducts(models.Model):
    vendor = models.ForeignKey(to=AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Categories, null=True, on_delete=models.CASCADE)
    price = models.FloatField()#models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(max_length=200, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to="img")
    image2 = models.ImageField(null=True, blank=True, upload_to="img")


    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Menu Products'
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
    @property
    def imageURL2(self):
        try:
            url = self.image2.url
        except:
            url = ''
        return url
    

class Order(models.Model):
    customer = models.ForeignKey(to=AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    ordered_items = models.ManyToManyField(MenuProducts, through="OrderItem")
    transaction_id = models.CharField(max_length=200, null=True)
    pending = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)

    date_ordered = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    
    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):   
    product = models.ForeignKey(MenuProducts, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
    def __str__(self):
        return str(self.order)
        
