# Generated by Django 3.1.2 on 2022-07-04 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0043_auto_20220617_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salereport',
            name='date_create',
            field=models.DateField(auto_now=True, verbose_name='Дата создания акта'),
        ),
    ]