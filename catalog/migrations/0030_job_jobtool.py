# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-24 15:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0029_auto_20180124_0818'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Job Name')),
                ('description', models.TextField(blank=True, help_text='Description of what the job entails', max_length=1000)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('directions', models.TextField(blank=True, help_text='Step by step instructions for this job', max_length=1000)),
                ('previousJob', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Job', verbose_name='Previous Required Job')),
                ('primdisc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='primdisc_job', to='catalog.Discipline', verbose_name='Primary Discipline')),
                ('secdisc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='secdisc_job', to='catalog.Discipline', verbose_name='Secondary Discipline')),
            ],
        ),
        migrations.CreateModel(
            name='JobTool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jobId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Job')),
                ('toolId', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='catalog.Tool')),
            ],
        ),
    ]
