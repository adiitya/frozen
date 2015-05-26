from django.contrib import admin
from dashboard.models import UserProfile, IPs, UserIpMap

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(IPs)
admin.site.register(UserIpMap)
