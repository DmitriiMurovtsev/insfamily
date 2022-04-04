# Generated by Django 3.1.2 on 2022-03-16 07:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_auto_20220314_1257'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bank',
            options={'verbose_name': 'Банк', 'verbose_name_plural': 'Банки'},
        ),
        migrations.CreateModel(
            name='Commission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_start', models.DateField(verbose_name='Дата начала действия')),
                ('value', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='КВ')),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.channel', verbose_name='Канал продаж')),
            ],
            options={
                'verbose_name': 'Входящее КВ',
                'verbose_name_plural': 'Входящее КВ',
            },
        ),
    ]
