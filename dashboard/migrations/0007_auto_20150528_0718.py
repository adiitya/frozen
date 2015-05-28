# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_auto_20150527_0923'),
    ]

    operations = [
        migrations.AddField(
            model_name='ips',
            name='status',
            field=models.CharField(default=None, max_length=1000),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_access',
            field=models.DateTimeField(default=datetime.datetime(1970, 1, 1, 0, 0), verbose_name=b'last access'),
        ),
    ]
