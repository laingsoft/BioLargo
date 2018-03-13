# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-12 21:31
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_timestamp', models.DateTimeField(auto_now_add=True)),
                ('edit_timestamp', models.DateTimeField(auto_now=True)),
                ('metadata', django.contrib.postgres.fields.jsonb.JSONField(default='')),
                ('friendly_name', models.CharField(max_length=255)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Company')),
                ('followers', models.ManyToManyField(blank=True, related_name='followed_experiments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ExperimentData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experimentData', django.contrib.postgres.fields.jsonb.JSONField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Company')),
                ('experiment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Experiment')),
            ],
            options={
                'verbose_name_plural': 'experiment data',
            },
        ),
        migrations.CreateModel(
            name='Fields',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('data_type', models.CharField(choices=[('INT', 'Integer'), ('FLOAT', 'Decimal'), ('DATE', 'Date'), ('STRING', 'Text')], default='STRING', max_length=6)),
                ('empty', models.CharField(blank=True, max_length=10)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Company')),
            ],
            options={
                'verbose_name_plural': 'fields',
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('predicate', models.CharField(choices=[('COM', 'commented on'), ('PRJ', 'uploaded a new experiment to'), ('UPD', 'updated experiment')], max_length=3)),
                ('object_type', models.CharField(choices=[('EXP', 'experiment'), ('PRJ', 'project')], max_length=3)),
                ('object_pk', models.IntegerField()),
                ('object_name', models.CharField(blank=True, max_length=255)),
                ('content', models.CharField(blank=True, max_length=255)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('read', models.BooleanField(default=False)),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activity', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Company')),
            ],
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Company')),
                ('fields', models.ManyToManyField(to='app.Fields')),
                ('metadata', models.ManyToManyField(related_name='metadata_fields', to='app.Fields')),
            ],
        ),
    ]
