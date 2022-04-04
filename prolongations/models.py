from django.db import models
from main.models import Client, Policy


class PolicyOnProlongation(models.Model):
    policy = models.ForeignKey(Policy, on_delete=models.DO_NOTHING, verbose_name='Полис', related_name='policy')
    policy_new = models.ForeignKey(Policy, on_delete=models.DO_NOTHING, verbose_name='Новый полис',
                                   related_name='policy_new', blank=True)
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING, verbose_name='Клиент')
    status = models.ForeignKey('Status', on_delete=models.DO_NOTHING, verbose_name='Статус')
    month = models.CharField(max_length=20, verbose_name='Месяц')

    class Meta:
        verbose_name = 'Полис'
        verbose_name_plural = 'Полисы'

    def __str__(self):
        return f'{self.month} {self.policy}'


class Status(models.Model):
    name = models.CharField(max_length=50, verbose_name='Статус', default='')
    extended = models.BooleanField(verbose_name='Продлён')

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

    def __str__(self):
        return self.name
