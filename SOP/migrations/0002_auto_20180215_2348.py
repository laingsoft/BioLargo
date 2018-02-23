# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-15 23:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('SOP', '0001_initial'),
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='opmaterials',
            name='Item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Item'),
        ),
        migrations.AddField(
            model_name='opmaterials',
            name='Op',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SOP.OperatingProcedure'),
        ),
    ]
