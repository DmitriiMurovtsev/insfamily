# Generated by Django 3.1.2 on 2022-04-18 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0036_auto_20220325_1459'),
    ]

    operations = [
        migrations.AddField(
            model_name='policy',
            name='type_pay',
            field=models.BooleanField(default=False, verbose_name='Наличка'),
        ),
    ]
