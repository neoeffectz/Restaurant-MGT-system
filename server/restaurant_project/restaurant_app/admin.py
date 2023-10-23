from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Customer)
admin.site.register(Categories)
admin.site.register(MenuProducts)
admin.site.register(Order)
admin.site.register(OrderItem)