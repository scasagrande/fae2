# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-06 13:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acct_type', models.IntegerField(choices=[(1, 'Standard'), (2, 'Level 2'), (3, 'Level 3'), (4, 'Level 4'), (5, 'Maximum')], default=1)),
                ('org', models.CharField(blank=True, max_length=128)),
                ('email_announcements', models.BooleanField(default=True)),
                ('multiple_urls_enabled', models.BooleanField(default=False)),
                ('website_authorization_enabled', models.BooleanField(default=False)),
                ('advanced_enabled', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, unique=True)),
            ],
        ),
    ]