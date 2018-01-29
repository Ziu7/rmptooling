# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-23 14:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0026_auto_20170915_1023'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discipline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter the discipline name', max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'Tool Discipline',
                'ordering': ['name'],
            },
        ),
        migrations.AlterModelOptions(
            name='location',
            options={'ordering': ['id'], 'permissions': (('can_add_location', 'Can add location'),)},
        ),
        migrations.AlterModelOptions(
            name='tool',
            options={'ordering': ['id', 'num'], 'permissions': (('can_edit_tool', 'Can edit Tool'),), 'verbose_name': 'Tool'},
        ),
        migrations.RenameField(
            model_name='location',
            old_name='location',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='historicaltoolsn',
            name='pm',
            field=models.CharField(choices=[('y', 'Yes'), ('n', 'No')], help_text='Is PM complete for this tool?', max_length=50),
        ),
        migrations.AlterField(
            model_name='historicaltoolsn',
            name='repair',
            field=models.CharField(choices=[('y', 'Yes'), ('n', 'No')], help_text='Does this tool need to be repaired?', max_length=5),
        ),
        migrations.AlterField(
            model_name='historicaltoolsn',
            name='vault',
            field=models.CharField(choices=[('y', 'Yes'), ('n', 'No')], help_text='Is this tool in the vault?', max_length=5, verbose_name='Stores in vault'),
        ),
        migrations.AlterField(
            model_name='tool',
            name='primdisc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='primdic_tool', to='catalog.Discipline', verbose_name='Primary Discipline'),
        ),
        migrations.AlterField(
            model_name='tool',
            name='secdisc',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='secdisc_tool', to='catalog.Discipline', verbose_name='Secondary Discipline'),
        ),
        migrations.AlterField(
            model_name='toolsn',
            name='pm',
            field=models.CharField(choices=[('y', 'Yes'), ('n', 'No')], help_text='Is PM complete for this tool?', max_length=50),
        ),
        migrations.AlterField(
            model_name='toolsn',
            name='repair',
            field=models.CharField(choices=[('y', 'Yes'), ('n', 'No')], help_text='Does this tool need to be repaired?', max_length=5),
        ),
        migrations.AlterField(
            model_name='toolsn',
            name='vault',
            field=models.CharField(choices=[('y', 'Yes'), ('n', 'No')], help_text='Is this tool in the vault?', max_length=5, verbose_name='Stores in vault'),
        ),
        migrations.DeleteModel(
            name='PrimDisc',
        ),
        migrations.DeleteModel(
            name='SecDisc',
        ),
    ]
