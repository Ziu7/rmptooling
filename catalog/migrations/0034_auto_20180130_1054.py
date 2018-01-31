# Generated by Django 2.0.1 on 2018-01-30 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0033_auto_20180129_0908'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vaultlog',
            options={'verbose_name': 'Tool Vault Log'},
        ),
        migrations.AlterField(
            model_name='vaultlog',
            name='borrowdate',
            field=models.DateField(verbose_name='time tool was checked out'),
        ),
        migrations.AlterField(
            model_name='vaultlog',
            name='returndate',
            field=models.DateField(verbose_name='time tool must be returned'),
        ),
    ]