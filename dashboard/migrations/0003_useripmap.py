# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_ips'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserIpMap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('polling_time', models.IntegerField(default=5)),
                ('client_id', models.ForeignKey(to='dashboard.UserProfile')),
                ('ip_id', models.ForeignKey(to='dashboard.IPs')),
            ],
        ),
    ]
