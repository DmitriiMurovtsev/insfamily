# Generated by Django 3.1.2 on 2022-06-08 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dscript', '0006_auto_20220608_1716'),
    ]

    operations = [
        migrations.AddField(
            model_name='step',
            name='text',
            field=models.TextField(default=1, verbose_name='Содержание'),
            preserve_default=False,
        ),
    ]
