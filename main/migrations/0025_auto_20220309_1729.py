# Generated by Django 3.1.2 on 2022-03-09 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_mortgagepolicy_client'),
    ]

    operations = [
        migrations.AddField(
            model_name='mortgagepolicy',
            name='msk',
            field=models.BooleanField(default=False, verbose_name='Москва'),
        ),
        migrations.AddField(
            model_name='mortgagepolicy',
            name='vlgd',
            field=models.BooleanField(default=False, verbose_name='Волгоград'),
        ),
    ]
