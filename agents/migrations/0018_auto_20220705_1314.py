# Generated by Django 3.1.2 on 2022-07-05 10:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0017_policyagents_company'),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Канал продаж')),
            ],
            options={
                'verbose_name': 'Канал продаж',
                'verbose_name_plural': 'Каналы продаж',
            },
        ),
        migrations.AddField(
            model_name='policyagents',
            name='channel',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='agents.channel', verbose_name='СК'),
            preserve_default=False,
        ),
    ]
