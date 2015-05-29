# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_ips_alive'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ip',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.GenericIPAddressField(verbose_name=b'ip_address')),
                ('last_access', models.DateTimeField(default=datetime.datetime(1970, 1, 1, 0, 0), verbose_name=b'last access')),
                ('min_poll_time', models.IntegerField(default=5)),
                ('status', models.CharField(max_length=1000, null=True, blank=True)),
                ('alive', models.BooleanField(default=True)),
            ],
        ),
        migrations.AlterField(
            model_name='useripmap',
            name='ip',
            field=models.ForeignKey(to='dashboard.Ip'),
        ),
        migrations.DeleteModel(
            name='IPs',
        ),
    ]
