# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('transact', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 27, 21, 50, 36, 918521, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 27, 21, 50, 44, 663237, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
