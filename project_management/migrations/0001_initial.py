# -*- coding: utf-8 -*-
<<<<<<< HEAD
# Generated by Django 1.11.10 on 2018-02-15 23:48
=======
# Generated by Django 1.11.10 on 2018-02-20 23:24
>>>>>>> b2066e29996fed2c4a55fa384d9be60a34002f1d
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('start', models.DateField()),
                ('end', models.DateField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Company')),
                ('followers', models.ManyToManyField(blank=True, related_name='followed_project', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=255)),
                ('complete', models.BooleanField(default=False)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('assigned', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to=settings.AUTH_USER_MODEL)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Company')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='project_management.Project')),
                ('related_experiment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Experiment')),
            ],
            options={
                'ordering': ['timestamp'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='task',
            unique_together=set([('project', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='project',
            unique_together=set([('company', 'name')]),
        ),
    ]
