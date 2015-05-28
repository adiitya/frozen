import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.db.models import Min

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

class Ip(models.Model):
    #Stores ip address to monitor
    name = models.GenericIPAddressField('ip_address')

    #Last time when status was fetched for this IP
    last_fetched = models.DateTimeField('last fetched', default = datetime.datetime(1970,1,1))

    #Time after which status is fetched for this IP
    min_poll_time = models.IntegerField(default = 5)

    #The status of this IP
    status = models.CharField(max_length=1000, null=True, blank=True)

    # Whether the IP is alive or not
    alive = models.BooleanField(default = True)

    def update_min_poll_time(self):
        data = UserIpMap.objects.filter(ip=self).aggregate(min_poll_time=Min('polling_time'))
        self.min_poll_time = data['min_poll_time']
        self.save();

class UserIpMap(models.Model):
    #This model specifies mapping betweeen user and IP being watched
    client = models.ForeignKey(User)
    ip = models.ForeignKey(Ip)
    polling_time = models.IntegerField(default = 5)