# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_auto_20150528_0718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ips',
            name='status',
            field=models.CharField(default=None, max_length=1000, blank=True),
        ),
    ]
