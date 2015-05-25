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