# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-08 20:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cooktopper', '0003_auto_20171101_2150'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='programmingdetails',
            name='new_burner_state',
        ),
        migrations.RemoveField(
            model_name='programmingdetails',
            name='temperature',
        ),
        migrations.RemoveField(
            model_name='programming',
            name='burner',
        ),
        migrations.RemoveField(
            model_name='programming',
            name='programming_details',
        ),
        migrations.RemoveField(
            model_name='shortcut',
            name='programming_details',
        ),
        migrations.AddField(
            model_name='programming',
            name='burner_state',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='cooktopper.BurnerState'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='programming',
            name='creation_time',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='programming',
            name='expected_duration',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='programming',
            name='programmed_time',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='programming',
            name='temperature',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='cooktopper.Temperature'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shortcut',
            name='programming',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='cooktopper.Programming'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='ProgrammingDetails',
        ),
    ]
