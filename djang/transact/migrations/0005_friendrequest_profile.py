# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transact', '0004_auto_20150430_1909'),
    ]

    operations = [
        migrations.CreateModel(
            name='FriendRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('recepient', models.ForeignKey(related_name='friendee', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(related_name='friendor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('friends', models.ManyToManyField(related_name='friends_rel_+', to='transact.Profile')),
                ('user', models.ForeignKey(related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
