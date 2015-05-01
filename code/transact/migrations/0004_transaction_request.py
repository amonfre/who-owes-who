# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transact', '0003_auto_20150429_0352'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='request',
            field=models.BooleanField(default=False),
        ),
    ]
