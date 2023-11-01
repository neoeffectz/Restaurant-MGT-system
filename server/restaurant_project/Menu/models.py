from django.db import models

# Create your models here.
class Categories(models.Model):
    name = models.CharField(max_length=200, null=True)
    image = models.ImageField(null=True, blank=True, upload_to="img/categories")
    
    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
    class Meta:
        verbose_name_plural = 'Categories'


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
    


