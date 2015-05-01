# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transact', '0008_auto_20150501_1001'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='networth',
            field=models.IntegerField(default=0),
        ),
    ]
