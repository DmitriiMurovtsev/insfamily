# Generated by Django 3.1.2 on 2022-05-23 09:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0040_delete_bso'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Наименование агента')),
                ('storage_time', models.IntegerField(verbose_name='Время хранения бланков')),
                ('date_at', models.DateField(auto_now_add=True, verbose_name='дата создания агента')),
            ],
            options={
                'verbose_name': 'Агент',
                'verbose_name_plural': 'Агенты',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='PolicyAgents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('policy', models.CharField(max_length=50, verbose_name='Полис')),
                ('client', models.CharField(max_length=100, verbose_name='Страхователь')),
                ('agent_commission', models.DecimalField(decimal_places=2, max_digits=5)),
                ('agent_commission_rub', models.DecimalField(decimal_places=2, max_digits=8)),
                ('date_registration', models.DateField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.company', verbose_name='Тип полиса')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.type', verbose_name='Тип полиса')),
            ],
        ),
        migrations.CreateModel(
            name='Bso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('series', models.CharField(blank=True, max_length=20, verbose_name='Серия')),
                ('number', models.CharField(max_length=30, verbose_name='Номер')),
                ('date_add', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('date_at', models.DateField(verbose_name='Дата выдачи')),
                ('agent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='bso', to='agents.agent', verbose_name='Агент')),
                ('company', models.ForeignKey(default='', on_delete=django.db.models.deletion.DO_NOTHING, related_name='bso', to='main.company', verbose_name='Страховая компания')),
            ],
            options={
                'verbose_name': 'БСО',
                'verbose_name_plural': 'БСО',
            },
        ),
    ]
