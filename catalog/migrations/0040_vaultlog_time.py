# Generated by Django 2.0.1 on 2018-01-31 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0039_auto_20180131_1020'),
    ]

    operations = [
        migrations.AddField(
            model_name='vaultlog',
            name='time',
            field=models.DateTimeField(auto_now=True, verbose_name='log of when action was done'),
        ),
    ]