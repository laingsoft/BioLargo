# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-25 19:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20180125_1853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='object_type',
            field=models.CharField(choices=[('EXP', 'Experiment'), ('PRJ', 'Project')], max_length=3),
        ),
        migrations.AlterField(
            model_name='notification',
            name='predicate',
            field=models.CharField(choices=[('COM', 'commented on'), ('PRJ', 'uploaded a new experiment to'), ('UPL', 'updated experiment')], max_length=3),
        ),
    ]
