# Generated by Django 2.0.1 on 2018-01-31 17:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0040_vaultlog_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='BorrowLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrowdate', models.DateField(verbose_name='time tool was checked out')),
                ('reason', models.BooleanField(default='0', verbose_name='why was tool taken out')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='logging Notes')),
                ('time', models.DateTimeField(auto_now=True, verbose_name='log of when action was done')),
                ('approvedby', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='manager_log', to=settings.AUTH_USER_MODEL, verbose_name='who approved the borrow')),
                ('borrower', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='borrower_log', to=settings.AUTH_USER_MODEL, verbose_name='tool loaned to')),
                ('toolsn', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='catalog.ToolSN', verbose_name='loaned tool')),
            ],
            options={
                'verbose_name': 'Tool Vault Log',
                'get_latest_by': ('borrowdate', 'id'),
            },
        ),
        migrations.AlterModelOptions(
            name='location',
            options={'ordering': ['name'], 'permissions': (('can_add_location', 'Can add location'),), 'verbose_name': 'Tool Locations'},
        ),
        migrations.AlterModelOptions(
            name='vaultlog',
            options={'get_latest_by': ('time', 'id'), 'verbose_name': 'Tool Vault Log'},
        ),
        migrations.RemoveField(
            model_name='vaultlog',
            name='approvedby',
        ),
        migrations.RemoveField(
            model_name='vaultlog',
            name='borrowdate',
        ),
        migrations.RemoveField(
            model_name='vaultlog',
            name='borrower',
        ),
        migrations.RemoveField(
            model_name='vaultlog',
            name='isreturned',
        ),
        migrations.RemoveField(
            model_name='vaultlog',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='vaultlog',
            name='returndate',
        ),
        migrations.AddField(
            model_name='vaultlog',
            name='invault',
            field=models.BooleanField(default='0', verbose_name='is the tool in the vault'),
        ),
        migrations.AlterField(
            model_name='tool',
            name='num',
            field=models.CharField(max_length=100, unique=True, verbose_name='tool no.'),
        ),
    ]
