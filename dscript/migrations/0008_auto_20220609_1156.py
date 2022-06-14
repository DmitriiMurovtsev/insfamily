# Generated by Django 3.1.2 on 2022-06-09 08:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dscript', '0007_step_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='step',
        ),
        migrations.RemoveField(
            model_name='step',
            name='text',
        ),
        migrations.AlterField(
            model_name='step',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Этап'),
        ),
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('count', models.IntegerField(verbose_name='Порядковый номер')),
                ('text', models.TextField(verbose_name='Содержание')),
                ('step', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dscript.step', verbose_name='Шаг')),
            ],
            options={
                'verbose_name': 'Шаг',
                'verbose_name_plural': 'Шаги',
            },
        ),
        migrations.AddField(
            model_name='answer',
            name='stage',
            field=models.ManyToManyField(related_name='answer', to='dscript.Stage', verbose_name='Шаг'),
        ),
    ]
