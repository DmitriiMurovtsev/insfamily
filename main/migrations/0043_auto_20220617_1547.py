# Generated by Django 3.1.2 on 2022-06-17 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0042_mortgagepolicy_type_mortgage'),
    ]

    operations = [
        migrations.CreateModel(
            name='SaleReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Наименование')),
                ('date_create', models.DateField(verbose_name='Дата создания акта')),
            ],
        ),
        migrations.CreateModel(
            name='Expenses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Наименование')),
                ('date_expenses', models.DateField(verbose_name='Дата расхода')),
                ('value', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Сумма расходов')),
                ('salary', models.BooleanField(default=False, verbose_name='Зарплата')),
                ('sale_report', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='main.salereport', verbose_name='АКТ')),
            ],
            options={
                'verbose_name': 'Расход',
                'verbose_name_plural': 'Расходы',
                'ordering': ['-date_expenses'],
            },
        ),
        migrations.AddField(
            model_name='policy',
            name='sale_report',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='main.salereport', verbose_name='АКТ'),
        ),
    ]
