# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-28 17:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='complete',
        ),
        migrations.RemoveField(
            model_name='task',
            name='in_progress',
        ),
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('N', 'Not started'), ('I', 'In progress'), ('C', 'Complete')], default='N', max_length=1),
        ),
    ]
