# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-12 18:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='permissiongroupcompany',
            name='description',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='permissiongroupcompany',
            name='group',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='extra', to='auth.Group'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='permissiongroupcompany',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Company'),
        ),
    ]
