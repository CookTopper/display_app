# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-05 18:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cooktopper', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='burner',
            name='time',
            field=models.IntegerField(default=1507228162),
            preserve_default=False,
        ),
    ]
