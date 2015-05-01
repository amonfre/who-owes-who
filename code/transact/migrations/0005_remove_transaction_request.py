# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transact', '0004_transaction_request'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='request',
        ),
    ]
