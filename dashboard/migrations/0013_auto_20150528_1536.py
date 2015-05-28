# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0012_auto_20150528_1531'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ip',
            name='last_access',
        ),
        migrations.AddField(
            model_name='ip',
            name='last_fetched',
            field=models.DateTimeField(default=datetime.datetime(1970, 1, 1, 0, 0), verbose_name=b'last fetched'),
        ),
    ]
