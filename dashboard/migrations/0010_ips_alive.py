# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_auto_20150528_0750'),
    ]

    operations = [
        migrations.AddField(
            model_name='ips',
            name='alive',
            field=models.BooleanField(default=True),
        ),
    ]
