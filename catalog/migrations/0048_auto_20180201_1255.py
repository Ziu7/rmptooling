# Generated by Django 2.0.1 on 2018-02-01 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0047_auto_20180131_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tool',
            name='minneeded',
            field=models.IntegerField(default='3', verbose_name='minimum tools requiried'),
        ),
    ]
