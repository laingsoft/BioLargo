# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-06 18:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('inventory', '0001_initial'),
        ('SOP', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sopmaterials',
            name='SOP',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Item'),
        ),
        migrations.AddField(
            model_name='sop',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Company'),
        ),
    ]