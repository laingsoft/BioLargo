# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-05 23:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SOP', '0002_auto_20180226_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sop',
            name='file',
            field=models.FileField(upload_to='SOP/'),
        ),
    ]