# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-26 18:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0031_auto_20180125_0857'),
    ]

    operations = [
        migrations.CreateModel(
            name='VaultLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrowdate', models.DateTimeField(verbose_name='time tool was checked out')),
                ('returndate', models.DateTimeField(verbose_name='time tool must be returned')),
                ('isreturned', models.BooleanField(verbose_name='has tool been returned')),
                ('approvedby', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='manager_log', to=settings.AUTH_USER_MODEL, verbose_name='who approved the borrow')),
                ('borrower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='borrower_log', to=settings.AUTH_USER_MODEL, verbose_name='tool loaned to')),
            ],
        ),
        migrations.AlterModelOptions(
            name='toolsn',
            options={'ordering': ['tool', 'sn'], 'verbose_name': 'Tool SN'},
        ),
        migrations.RemoveField(
            model_name='historicaltoolsn',
            name='borrower',
        ),
        migrations.RemoveField(
            model_name='historicaltoolsn',
            name='vault',
        ),
        migrations.RemoveField(
            model_name='historicaltoolsn',
            name='vaultintime',
        ),
        migrations.RemoveField(
            model_name='historicaltoolsn',
            name='vaultouttime',
        ),
        migrations.RemoveField(
            model_name='toolsn',
            name='borrower',
        ),
        migrations.RemoveField(
            model_name='toolsn',
            name='vault',
        ),
        migrations.RemoveField(
            model_name='toolsn',
            name='vaultintime',
        ),
        migrations.RemoveField(
            model_name='toolsn',
            name='vaultouttime',
        ),
        migrations.AlterField(
            model_name='historicaltoolsn',
            name='checkdate',
            field=models.DateTimeField(null='True', verbose_name='time when tool was checked'),
        ),
        migrations.AlterField(
            model_name='historicaltoolsn',
            name='pm',
            field=models.BooleanField(help_text='Is PM complete for this tool?', max_length=50),
        ),
        migrations.AlterField(
            model_name='historicaltoolsn',
            name='repair',
            field=models.BooleanField(help_text='Does this tool need to be repaired?', max_length=5),
        ),
        migrations.AlterField(
            model_name='historicaltoolsn',
            name='sn',
            field=models.CharField(max_length=10, verbose_name='tool SN'),
        ),
        migrations.AlterField(
            model_name='job',
            name='name',
            field=models.CharField(max_length=200, verbose_name='job name'),
        ),
        migrations.AlterField(
            model_name='job',
            name='previousJob',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Job', verbose_name='previous required job'),
        ),
        migrations.AlterField(
            model_name='job',
            name='primdisc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='primdisc_job', to='catalog.Discipline', verbose_name='primary discipline'),
        ),
        migrations.AlterField(
            model_name='job',
            name='secdisc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='secdisc_job', to='catalog.Discipline', verbose_name='secondary discipline'),
        ),
        migrations.AlterField(
            model_name='location',
            name='address',
            field=models.CharField(default='N/A', max_length=200, verbose_name='street address'),
        ),
        migrations.AlterField(
            model_name='location',
            name='name',
            field=models.CharField(help_text='Enter tool location.', max_length=200, unique=True, verbose_name='location Name'),
        ),
        migrations.AlterField(
            model_name='tool',
            name='draw',
            field=models.CharField(blank=True, max_length=200, verbose_name='tool drawing(s)'),
        ),
        migrations.AlterField(
            model_name='tool',
            name='minneeded',
            field=models.IntegerField(default='0', verbose_name='minimum tools requiried'),
        ),
        migrations.AlterField(
            model_name='tool',
            name='name',
            field=models.CharField(max_length=200, verbose_name='tool name'),
        ),
        migrations.AlterField(
            model_name='tool',
            name='primdisc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='primdic_tool', to='catalog.Discipline', verbose_name='primary discipline'),
        ),
        migrations.AlterField(
            model_name='tool',
            name='secdisc',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='secdisc_tool', to='catalog.Discipline', verbose_name='secondary discipline'),
        ),
        migrations.AlterField(
            model_name='toolsn',
            name='checkdate',
            field=models.DateTimeField(null='True', verbose_name='time when tool was checked'),
        ),
        migrations.AlterField(
            model_name='toolsn',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Location', verbose_name='location of the tool'),
        ),
        migrations.AlterField(
            model_name='toolsn',
            name='pm',
            field=models.BooleanField(help_text='Is PM complete for this tool?', max_length=50),
        ),
        migrations.AlterField(
            model_name='toolsn',
            name='repair',
            field=models.BooleanField(help_text='Does this tool need to be repaired?', max_length=5),
        ),
        migrations.AlterField(
            model_name='toolsn',
            name='sn',
            field=models.CharField(max_length=10, verbose_name='tool SN'),
        ),
        migrations.AlterField(
            model_name='toolsn',
            name='tool',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Tool', verbose_name='tool no.'),
        ),
        migrations.AddField(
            model_name='vaultlog',
            name='toolsn',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.ToolSN', verbose_name='loaned tool'),
        ),
    ]
