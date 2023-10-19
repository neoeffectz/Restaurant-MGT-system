
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.

#The below model can be used for orders online
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True,blank=True)
    email = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

@receiver(post_save, sender=User)
def create_customer(sender, instance, created, *args, **kwargs):
    if created:
        Customer.objects.create(user=instance, email=instance.email, name=instance.user_name)
        print(instance, 'customer created')


@receiver(post_save, sender=User)
def save_customer(sender, instance, *args, **kwargs):
    instance.customer.save()


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
    vendor = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
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
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
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
        
