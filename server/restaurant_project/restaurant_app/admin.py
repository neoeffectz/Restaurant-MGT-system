from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm


# Customized the admin panel to include other fields upon registration
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("email", "is_staff", "is_active", "first_name", "last_name", "phone_number",)
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "phone_number",)}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions",
                "first_name", "last_name", "phone_number", "role"  
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Categories)
admin.site.register(MenuProducts)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Amenity)
admin.site.register(Hotel)
admin.site.register(Reservation)