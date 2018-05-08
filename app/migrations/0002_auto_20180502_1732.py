# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-02 17:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project_management', '0001_initial'),
        ('accounts', '0001_initial'),
        ('app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('SOP', '0002_auto_20180502_1732'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_management.Project'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='sop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='SOP.SOP'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='tags',
            field=models.ManyToManyField(to='app.Tag'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Company'),
        ),
        migrations.AddField(
            model_name='comment',
            name='experiment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Experiment'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='template',
            unique_together=set([('company', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='tag',
            unique_together=set([('company', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='fields',
            unique_together=set([('company', 'name')]),
        ),
    ]