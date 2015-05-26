# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_useripmap'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ips',
            name='last_access',
            field=models.DateTimeField(default=datetime.datetime(1970, 1, 1, 0, 0), verbose_name=b'last access'),
        ),
    ]
