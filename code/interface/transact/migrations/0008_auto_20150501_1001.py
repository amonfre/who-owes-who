# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transact', '0007_profile_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('recepient', models.ForeignKey(related_name='trecepient', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(related_name='tsender', to=settings.AUTH_USER_MODEL)),
                ('transaction', models.ForeignKey(related_name='request', to='transact.Transaction')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='friendrequest',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 1, 10, 0, 59, 544217, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='friendrequest',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 1, 10, 1, 3, 480531, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 1, 10, 1, 8, 242056, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 1, 10, 1, 12, 192010, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
