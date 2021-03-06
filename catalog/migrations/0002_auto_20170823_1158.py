# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-23 15:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(help_text='Enter tool location.', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ToolSN',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for tool', primary_key=True, serialize=False)),
                ('sn', models.CharField(max_length=10)),
                ('pm', models.CharField(choices=[('complete', 'complete'), ('incomplete', 'complete')], help_text='Is PM complete for this tool?', max_length=50)),
                ('repair', models.CharField(choices=[('y', 'yes'), ('n', 'no')], help_text='Does this tool need to be repaired?', max_length=5)),
                ('checkdate', models.DateField(blank=True, null=True)),
                ('comments', models.TextField(blank=True, help_text='Enter any comments for this tool as necessary.', max_length=1000)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Location')),
            ],
            options={
                'ordering': ['tool'],
            },
        ),
        migrations.RenameField(
            model_name='tool',
            old_name='tooldraw',
            new_name='draw',
        ),
        migrations.RenameField(
            model_name='tool',
            old_name='toolname',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='tool',
            old_name='toolnum',
            new_name='num',
        ),
        migrations.RemoveField(
            model_name='tool',
            name='toolnotes',
        ),
        migrations.AddField(
            model_name='tool',
            name='notes',
            field=models.TextField(blank=True, help_text='Enter any notes for this tool as necessary.', max_length=1000),
        ),
        migrations.AddField(
            model_name='toolsn',
            name='tool',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Tool'),
        ),
    ]
