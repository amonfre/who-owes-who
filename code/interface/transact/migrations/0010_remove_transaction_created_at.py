# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transact', '0009_profile_networth'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='created_at',
        ),
    ]
