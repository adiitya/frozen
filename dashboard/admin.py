from django.contrib import admin
from dashboard.models import UserProfile, Ip, UserIpMap

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Ip)
admin.site.register(UserIpMap)
