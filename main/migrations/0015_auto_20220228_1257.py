# Generated by Django 3.1.2 on 2022-02-28 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20220227_1417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='email',
            field=models.EmailField(blank=True, max_length=100, null=True, verbose_name='Почта'),
        ),
        migrations.AlterField(
            model_name='client',
            name='phone',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Телефон'),
        ),
    ]
