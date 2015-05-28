# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0011_auto_20150528_1522'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ip',
            old_name='ip',
            new_name='name',
        ),
    ]
