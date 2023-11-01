from django.db import models

# Create your models here.
class Amenity(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    

    class Meta:
        verbose_name_plural = 'Amenity'
