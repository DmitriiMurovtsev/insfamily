# Generated by Django 3.1.2 on 2022-02-27 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_policy_prolong'),
    ]

    operations = [
        migrations.AlterField(
            model_name='policy',
            name='prolong',
            field=models.BooleanField(default=False, verbose_name='Пролонгация'),
        ),
    ]
