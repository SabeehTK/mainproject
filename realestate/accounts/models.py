from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import secrets
# Create your models here.
class Profile(models.Model):
    USER_ROLES = [
        ('buyer', 'Buyer'),
        ('agent', 'Agent'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=USER_ROLES, default='buyer')
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)


    def __str__(self):
        return f"{self.user.username} - {self.role}"

class EmailOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() < self.created_at + timedelta(minutes=5)

    def generate_otp(self):
        otp= str(secrets.randbelow(1000000)).zfill(6)  # 6-digit OTP
        self.code = otp
        self.save()

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name


# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
# @receiver(post_save, sender=User)
# def create_or_update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#     instance.profile.save()

