# -*- coding: utf-8 -*-
<<<<<<< HEAD
# Generated by Django 1.11.10 on 2018-02-15 23:48
=======
# Generated by Django 1.11.10 on 2018-02-20 23:24
>>>>>>> b2066e29996fed2c4a55fa384d9be60a34002f1d
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SOP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=255)),
                ('file', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='SOPMaterials',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('unit', models.CharField(choices=[('L', 'L'), ('g', 'g'), ('mL', 'mL')], max_length=3)),
            ],
        ),
    ]
