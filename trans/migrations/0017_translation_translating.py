# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-12-26 08:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trans', '0016_auto_20180822_0510'),
    ]

    operations = [
        migrations.AddField(
            model_name='translation',
            name='translating',
            field=models.BooleanField(null=True),
        ),
    ]
