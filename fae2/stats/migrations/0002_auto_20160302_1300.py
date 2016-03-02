# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-02 19:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='statsusers',
            options={'verbose_name': 'Registered Users', 'verbose_name_plural': 'Registered Users'},
        ),
        migrations.RemoveField(
            model_name='statsuser',
            name='stats_users',
        ),
        migrations.AddField(
            model_name='statsusers',
            name='user_stats',
            field=models.ManyToManyField(blank=True, default=None, related_name='stats_users', to='stats.StatsUser'),
        ),
    ]
