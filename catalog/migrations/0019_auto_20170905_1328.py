# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-05 17:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0018_auto_20170831_1305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='toolsn',
            name='pm',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], help_text='Is PM complete for this tool?', max_length=50),
        ),
        migrations.AlterField(
            model_name='toolsn',
            name='repair',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], help_text='Does this tool need to be repaired?', max_length=5),
        ),
    ]
