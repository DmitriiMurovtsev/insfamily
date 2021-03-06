# Generated by Django 3.1.2 on 2022-07-04 10:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0007_auto_20220704_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bso',
            name='agent',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, related_name='bso', to='agents.agent', verbose_name='Агент'),
        ),
        migrations.AlterField(
            model_name='bso',
            name='date_at',
            field=models.DateField(default=None, verbose_name='Дата выдачи агенту'),
        ),
    ]
