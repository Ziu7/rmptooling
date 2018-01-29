# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-24 02:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0010_auto_20170823_1430'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='primdisc',
            options={'ordering': ['primary'], 'verbose_name': 'Primary Discipline'},
        ),
        migrations.AlterModelOptions(
            name='secdisc',
            options={'ordering': ['secondary'], 'verbose_name': 'Secondary Discipline'},
        ),
        migrations.AlterModelOptions(
            name='tool',
            options={'verbose_name': 'Tool'},
        ),
        migrations.AlterModelOptions(
            name='toolsn',
            options={'ordering': ['tool'], 'verbose_name': 'Tool SN'},
        ),
        migrations.AddField(
            model_name='tool',
            name='toolpic',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]