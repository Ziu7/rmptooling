# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-25 17:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0013_auto_20170825_0835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='toolsn',
            name='pm',
            field=models.CharField(choices=[('YES', 'YES'), ('NO', 'NO')], help_text='Is PM complete for this tool?', max_length=50),
        ),
        migrations.AlterField(
            model_name='toolsn',
            name='repair',
            field=models.CharField(choices=[('YES', 'YES'), ('NO', 'NO')], help_text='Does this tool need to be repaired?', max_length=5),
        ),
    ]
