# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-08-29 13:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trans', '0017_auto_20200829_0807'),
    ]

    operations = [
        migrations.AddField(
            model_name='translation',
            name='not_translating',
            field=models.BooleanField(default=False),
        ),
    ]
