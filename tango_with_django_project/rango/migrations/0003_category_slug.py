# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-17 21:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0002_auto_20180317_2100'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
