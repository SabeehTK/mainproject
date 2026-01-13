from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Property(models.Model):
    PROPERTY_TYPES = [
        ('plot', 'Plot'),
        ('flat', 'Flat'),
        ('house', 'House'),
    ]
    REQUIREMENT_TYPES = [
        ('for sale', 'For Sale'),
        ('for rent', 'For Rent'),
    ]
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    location = models.CharField(max_length=100)
    property_type = models.CharField(max_length=10, choices=PROPERTY_TYPES)
    requirement=models.CharField(choices=REQUIREMENT_TYPES)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='property_images/')
    owner = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user')
    def __str__(self):
        return self.title

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
