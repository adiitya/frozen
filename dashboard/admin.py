from django.contrib import admin
from dashboard.models import UserProfile, IPs

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(IPs)
