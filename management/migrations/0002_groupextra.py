# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-15 18:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        ('accounts', '0003_auto_20180115_1849'),
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupExtra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=255)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Company')),
                ('group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='extra', to='auth.Group')),
            ],
        ),
    ]
