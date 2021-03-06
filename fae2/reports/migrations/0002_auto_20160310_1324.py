# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-10 19:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='websitereport',
            name='first_page_url',
        ),
        migrations.RemoveField(
            model_name='websitereport',
            name='last_first_page',
        ),
        migrations.RemoveField(
            model_name='websitereport',
            name='last_last_page',
        ),
        migrations.RemoveField(
            model_name='websitereport',
            name='last_next_page',
        ),
        migrations.RemoveField(
            model_name='websitereport',
            name='last_page_url',
        ),
        migrations.RemoveField(
            model_name='websitereport',
            name='last_prev_page',
        ),
        migrations.RemoveField(
            model_name='websitereport',
            name='next_page_url',
        ),
        migrations.RemoveField(
            model_name='websitereport',
            name='prev_page_url',
        ),
        migrations.AddField(
            model_name='websitereport',
            name='last_group',
            field=models.CharField(default=b'', max_length=32, verbose_name=b'Last View'),
        ),
        migrations.AddField(
            model_name='websitereport',
            name='last_report_type',
            field=models.CharField(choices=[(b'rules', b'Summary'), (b'pages', b'All Pages'), (b'page', b'Page')], default=b'rules', max_length=16, verbose_name=b'Last View'),
        ),
        migrations.AlterField(
            model_name='websitereport',
            name='last_view',
            field=models.CharField(choices=[(b'rc', b'Rule Category'), (b'gl', b'WCAG Guideline'), (b'rs', b'Rule Scope')], default=b'rc', max_length=4, verbose_name=b'Last View'),
        ),
    ]
