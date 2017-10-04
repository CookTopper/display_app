# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-26 19:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Burner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='BurnerState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Pan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=45)),
                ('temperature', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PanState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Programming',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('burner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cooktopper.Burner')),
            ],
        ),
        migrations.CreateModel(
            name='ProgrammingDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('programmed_hour', models.CharField(max_length=45)),
                ('expected_duration', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ProgrammingType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Shortcut',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=45)),
                ('programming_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cooktopper.ProgrammingDetails')),
            ],
        ),
        migrations.CreateModel(
            name='Stove',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Temperature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=45)),
            ],
        ),
        migrations.AddField(
            model_name='programmingdetails',
            name='programming_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cooktopper.ProgrammingType'),
        ),
        migrations.AddField(
            model_name='programmingdetails',
            name='temperature',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cooktopper.Temperature'),
        ),
        migrations.AddField(
            model_name='programming',
            name='programming_details',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cooktopper.ProgrammingDetails'),
        ),
        migrations.AddField(
            model_name='pan',
            name='pan_state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cooktopper.PanState'),
        ),
        migrations.AddField(
            model_name='burner',
            name='burner_state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cooktopper.BurnerState'),
        ),
        migrations.AddField(
            model_name='burner',
            name='stove',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cooktopper.Stove'),
        ),
        migrations.AddField(
            model_name='burner',
            name='temperature',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cooktopper.Temperature'),
        ),
    ]