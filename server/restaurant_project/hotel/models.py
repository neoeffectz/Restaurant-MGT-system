from django.db import models
from Amenity.models import Amenity
from django_tenants.models import TenantMixin, DomainMixin

# Create your models here.
class Hotel(TenantMixin):
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    has_tables = models.BooleanField(default=False)
    amenities = models.ManyToManyField(Amenity, related_name='hotels')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True


    def __str__(self):
        return self.name
    

    class Meta:
        verbose_name_plural = 'Hotel'


class Domain(DomainMixin):
    pass