# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transact', '0003_transaction_accepted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='accepted',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
