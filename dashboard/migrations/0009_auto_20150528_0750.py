# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_auto_20150528_0747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ips',
            name='status',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
    ]
