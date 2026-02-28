from django.contrib import admin
from listing.models import Property
from listing.models import Enquiry

from listing.models import Payment

# Register your models here.
admin.site.register(Property)
admin.site.register(Enquiry)
admin.site.register(Payment)
