# Generated by Django 2.0.1 on 2018-01-30 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0035_auto_20180130_1340'),
    ]

    operations = [
        migrations.AddField(
            model_name='vaultlog',
            name='notes',
            field=models.TextField(blank=True, null=True, verbose_name='Logging Notes'),
        ),
    ]