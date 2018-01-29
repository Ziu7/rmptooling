# Generated by Django 2.0.1 on 2018-01-29 14:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0032_auto_20180126_1328'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicaltoolsn',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicaltoolsn',
            name='location',
        ),
        migrations.RemoveField(
            model_name='historicaltoolsn',
            name='tool',
        ),
        migrations.AlterField(
            model_name='job',
            name='previousJob',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.Job', verbose_name='previous required job'),
        ),
        migrations.AlterField(
            model_name='job',
            name='primdisc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='primdisc_job', to='catalog.Discipline', verbose_name='primary discipline'),
        ),
        migrations.AlterField(
            model_name='job',
            name='secdisc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='secdisc_job', to='catalog.Discipline', verbose_name='secondary discipline'),
        ),
        migrations.AlterField(
            model_name='tool',
            name='primdisc',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='primdic_tool', to='catalog.Discipline', verbose_name='primary discipline'),
        ),
        migrations.AlterField(
            model_name='tool',
            name='secdisc',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='secdisc_tool', to='catalog.Discipline', verbose_name='secondary discipline'),
        ),
        migrations.AlterField(
            model_name='toolsn',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.Location', verbose_name='location of the tool'),
        ),
        migrations.AlterField(
            model_name='vaultlog',
            name='borrower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='borrower_log', to=settings.AUTH_USER_MODEL, verbose_name='tool loaned to'),
        ),
        migrations.AlterField(
            model_name='vaultlog',
            name='toolsn',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='catalog.ToolSN', verbose_name='loaned tool'),
        ),
        migrations.DeleteModel(
            name='HistoricalToolSN',
        ),
    ]