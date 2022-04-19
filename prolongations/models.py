from django.db import models

from main.models import Type, Company, Client


class PolicyBase(models.Model):
    type = models.ForeignKey(Type, on_delete=models.DO_NOTHING, related_name='policy_base', verbose_name='Тип полиса')
    name = models.ForeignKey('NameBase', on_delete=models.DO_NOTHING, related_name='policy_base',
                             verbose_name='Название', null=True, blank=True)
    company = models.ForeignKey(
        Company, on_delete=models.DO_NOTHING, related_name='policy_base', verbose_name='Компания')
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING, related_name='policy_base', verbose_name='Клиент')
    status = models.ForeignKey(
        'Status', on_delete=models.DO_NOTHING, related_name='policy_base', verbose_name='Статус', null=True, blank=True)
    bso = models.CharField(max_length=50, verbose_name='БСО')
    sp = models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Страховая премия')
    channel = models.CharField(max_length=50, verbose_name='Канал продаж')
    date_end = models.CharField(max_length=50, verbose_name='Дата окончания')
    manager = models.CharField(max_length=50, verbose_name='Менеджер прошлого года')
    object = models.CharField(max_length=50, verbose_name='Объект страхования')


class Status(models.Model):
    name = models.CharField(max_length=50, verbose_name='Статус')

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

    def __str__(self):
        return self.name


class NameBase(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название базы')

    def __str__(self):
        return self.name
