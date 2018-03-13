# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-12 21:31
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('auth', '0008_alter_user_username_max_length'),
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
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateformat', models.CharField(choices=[('YYYY-MM-DD', 'YYYY-MM-DD'), ('MM-DD-YYYY', 'MM-DD-YYYY'), ('DD-MM-YYYY', 'DD-MM-YYYY')], default='YYYY-MM-DD', max_length=11)),
                ('ataglance', django.contrib.postgres.fields.jsonb.JSONField(default={})),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Company')),
            ],
        ),
    ]
