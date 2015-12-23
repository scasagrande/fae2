# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-23 20:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0003_auto_20151223_1355'),
    ]

    operations = [
        migrations.AddField(
            model_name='websitereport',
            name='last_next_page_url',
            field=models.URLField(blank=True, default='', max_length=1024, verbose_name='Next Page URL'),
        ),
        migrations.AddField(
            model_name='websitereport',
            name='last_prev_page_url',
            field=models.URLField(blank=True, default='', max_length=1024, verbose_name='Previous Page URL'),
        ),
        migrations.AlterField(
            model_name='websitereport',
            name='last_next_page',
            field=models.IntegerField(default=0, verbose_name='Next Page Number'),
        ),
        migrations.AlterField(
            model_name='websitereport',
            name='last_prev_page',
            field=models.IntegerField(default=0, verbose_name='Previous Page Number'),
        ),
    ]
