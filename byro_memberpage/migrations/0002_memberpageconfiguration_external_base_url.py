# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-26 21:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('byro_memberpage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='memberpageconfiguration',
            name='external_base_url',
            field=models.CharField(blank=True, help_text='This field is used to generate the absolute URL for memberpage addresses.', max_length=512, null=True, verbose_name='External base URL of byro installation'),
        ),
    ]
