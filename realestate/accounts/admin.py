from django.contrib import admin
from accounts.models import Profile
from accounts.models import EmailOTP, Contact

# Register your models here.
admin.site.register(Profile)
admin.site.register(EmailOTP)
admin.site.register(Contact)
