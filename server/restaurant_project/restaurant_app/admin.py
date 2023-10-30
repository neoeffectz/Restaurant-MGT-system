from django.contrib import admin

# Register your models here.
from .models import Customer, Categories, MenuProducts, Order, OrderItem, Hotel, Amenity, Reservation


admin.site.register(Customer)
admin.site.register(Categories)
admin.site.register(MenuProducts)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Hotel)
admin.site.register(Amenity)
admin.site.register(Reservation)
