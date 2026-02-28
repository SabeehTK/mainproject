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
    price = models.IntegerField()
    location = models.CharField(max_length=100)
    property_type = models.CharField(max_length=10, choices=PROPERTY_TYPES)
    requirement=models.CharField(choices=REQUIREMENT_TYPES)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='property_images/')
    owner = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user')
    def __str__(self):
        return self.title

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='wishlist')
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

class Enquiry(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE,related_name='enquiry')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(default='eg@example.com')
    phone_number = models.CharField(max_length=11,default='00000')
    message = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    status_choices = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),]
    status = models.CharField(choices=status_choices, default='pending', max_length=10)
    visiting_date = models.DateTimeField(null=True, blank=True)
    agent_response = models.TextField(null=True, blank=True)
    buyer_visited=models.BooleanField(default=False)
    buyer_rejected=models.BooleanField(default=False)
    def __str__(self):
        return f"{self.property.title} - {self.status}"

    def is_advance_paid(self):
        return self.payment.filter(status='success').exists()

class Payment(models.Model):
    enquiry = models.ForeignKey(Enquiry, on_delete=models.CASCADE,null=True,related_name='payment')
    razorpay_order_id = models.CharField(max_length=100, unique=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)
    amount = models.IntegerField()
    paid_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    status_choices = [
        ('created', 'Created'),
        ('success', 'Success'),
        ('failed', 'Failed'),]
    status = models.CharField(max_length=10,choices=status_choices, default='created')
    created_at = models.DateTimeField(auto_now_add=True)