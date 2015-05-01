# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transact', '0002_auto_20150427_2150'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
    ]
