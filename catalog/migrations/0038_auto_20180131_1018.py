# Generated by Django 2.0.1 on 2018-01-31 15:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0037_auto_20180131_0823'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vaultlog',
            options={'get_latest_by': ('borrowdate', '-id'), 'verbose_name': 'Tool Vault Log'},
        ),
    ]
