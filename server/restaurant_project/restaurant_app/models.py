from django.db import models
from restaurant_project.settings import AUTH_USER_MODEL
<<<<<<< Updated upstream



#used the base user to replace the username with email as the authentication
class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, password, first_name, last_name, phone_number, **extra_fields):

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
    first_name = models.CharField("First Name", max_length=30, null=False)
    last_name = models.CharField("Last Name", max_length=30, null=True, blank=True)
    phone_number = models.CharField(
        "Phone Number", max_length=20, null=False, unique=True
    )

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
    

=======
from hotel.models import Hotel
from Menu.models import MenuProducts
User = AUTH_USER_MODEL



class Reservation(models.Model):
    guest = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    number_of_adults = models.PositiveSmallIntegerField()
    number_of_children = models.PositiveSmallIntegerField()
    special_requests = models.TextField(blank=True, null=True)
    is_confirmed = models.BooleanField(default=False)
    table_number = models.CharField(max_length=10, null=True, blank=True)
    table_type = models.CharField(max_length=50, null=True, blank=True)
    is_available = models.BooleanField(default=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.guest
    
    class Meta:
        verbose_name_plural = 'Reservation'


>>>>>>> Stashed changes
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
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
        
