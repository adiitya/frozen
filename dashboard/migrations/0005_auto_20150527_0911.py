# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_auto_20150525_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useripmap',
            name='client_id',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
