# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_auto_20150527_0911'),
    ]

    operations = [
        migrations.RenameField(
            model_name='useripmap',
            old_name='client_id',
            new_name='client',
        ),
        migrations.RenameField(
            model_name='useripmap',
            old_name='ip_id',
            new_name='ip',
        ),
    ]
