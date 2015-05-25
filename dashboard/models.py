from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    # Links UserProfile to an actual User model
    user = models.OneToOneField(User)

    # The last access time of the user
    last_access = models.DateTimeField('last access')

    # Whether the user is alive or not
    alive = models.BooleanField(default = False)

class IPs(models.Model):
	#Stores ip address to monitor
	ip = models.GenericIPAddressField('ip_address')

	#Last time when status was fetched for this IP
	last_access = models.DateTimeField('last access')

	#Time after which status is fetched for this IP
	min_poll_time = models.IntegerField(default = 5)

class UserIpMap(models.Model):
	#This model specifies mapping betweeen user and IP being watched
	client_id = models.ForeignKey(UserProfile)
	ip_id = models.ForeignKey(IPs)
	polling_time = models.IntegerField(default = 5)