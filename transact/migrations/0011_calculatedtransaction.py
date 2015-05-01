# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transact', '0010_remove_transaction_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='CalculatedTransaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('amount', models.FloatField()),
                ('recepient', models.ForeignKey(related_name='recepientc', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(related_name='senderc', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
