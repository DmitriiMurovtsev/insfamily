# Generated by Django 3.1.2 on 2022-06-09 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dscript', '0008_auto_20220609_1156'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='negative',
            field=models.BooleanField(default=False, verbose_name='Позитивный ответ'),
        ),
        migrations.AddField(
            model_name='answer',
            name='neutral',
            field=models.BooleanField(default=True, verbose_name='Позитивный ответ'),
        ),
        migrations.AddField(
            model_name='answer',
            name='positive',
            field=models.BooleanField(default=False, verbose_name='Позитивный ответ'),
        ),
    ]