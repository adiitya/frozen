import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

# Create your models here.

class UserProfile(models.Model):
    # Links UserProfile to an actual User model
    user = models.OneToOneField(User)

    # The last access time of the user
    last_access = models.DateTimeField('last access', default = datetime.datetime(1970,1,1))

    # Whether the user is alive or not
    alive = models.BooleanField(default = False)

    @receiver(post_save, sender=User)
    def create_profile_for_user(sender, instance=None, created=False, **kwargs):	
        if created:
            UserProfile.objects.get_or_create(user=instance)

    @receiver(pre_delete, sender=User)
    def delete_profile_for_user(sender, instance=None, **kwargs):
        if instance:
            user_profile = UserProfile.objects.get(user=instance)
            user_profile.delete()

class IPs(models.Model):
	#Stores ip address to monitor
	ip = models.GenericIPAddressField('ip_address')

	#Last time when status was fetched for this IP
	last_access = models.DateTimeField('last access', default = datetime.datetime(1970,1,1))

	#Time after which status is fetched for this IP
	min_poll_time = models.IntegerField(default = 5)

class UserIpMap(models.Model):
	#This model specifies mapping betweeen user and IP being watched
	client_id = models.ForeignKey(UserProfile)
	ip_id = models.ForeignKey(IPs)
	polling_time = models.IntegerField(default = 5)