from django.db import models

from main.models import Company, Type


class Bso(models.Model):
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, related_name='bso',
                                verbose_name='Страховая компания', default='')
    series = models.CharField(max_length=20, verbose_name='Серия', blank=True)
    number = models.CharField(max_length=30, verbose_name='Номер')
    agent = models.ForeignKey('Agent', on_delete=models.DO_NOTHING, related_name='bso', verbose_name='Агент',
                              blank=True, null=True)
    date_add = models.DateField(verbose_name='Дата получения от СК')
    date_at = models.DateField(verbose_name='Дата выдачи агенту', blank=True, null=True)
    clear = models.BooleanField(verbose_name='Чистый бланк', default=True)

    class Meta:
        verbose_name = 'БСО'
        verbose_name_plural = 'БСО'
        ordering = ['date_at']

    def __str__(self):
        return f'{self.series} {self.number}'


class Agent(models.Model):
    name = models.CharField(max_length=50, verbose_name='Наименование агента')
    storage_time = models.IntegerField(verbose_name='Время хранения бланков')
    date_at = models.DateField(auto_now_add=True, verbose_name='дата создания агента')

    class Meta:
        verbose_name = 'Агент'
        verbose_name_plural = 'Агенты'
        ordering = ['name']

    def __str__(self):
        return self.name


class PolicyAgents(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.DO_NOTHING, verbose_name='Агент', related_name='policy')
    type = models.ForeignKey(Type, verbose_name='Тип полиса', on_delete=models.DO_NOTHING)
    policy = models.CharField(max_length=50, verbose_name='Полис')
    client = models.CharField(max_length=100, verbose_name='Страхователь')
    type_client = models.CharField(max_length=20, verbose_name='Тип страхователя')
    agent_commission = models.DecimalField(decimal_places=2, max_digits=5)
    agent_commission_rub = models.DecimalField(decimal_places=2, max_digits=8)
    date_registration = models.DateField(verbose_name='Дата подписания договора')
    date_start = models.DateField(verbose_name='Дата начала действия')
    date_end = models.DateField(verbose_name='Дата окончания действия')
    price = models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Общая премия')
    type_pay = models.CharField(max_length=20, verbose_name='Тип оплаты')
    status = models.CharField(max_length=20, verbose_name='Статус полиса', default='reconciliation')

    class Meta:
        verbose_name = 'Полис'
        verbose_name_plural = 'Полисы'
        ordering = ['-date_registration']

    def __str__(self):
        return self.policy


class HistoryBso(models.Model):
    # История изменений БСО
    date_at = models.DateField(verbose_name='Дата изменения статуса бланка')
    status = models.ForeignKey('StatusBso', on_delete=models.CASCADE, verbose_name='Статус полиса')
    bso = models.ForeignKey(Bso, on_delete=models.CASCADE, verbose_name='БСО', related_name='history')

    class Meta:
        verbose_name = 'История БСО'
        verbose_name_plural = 'История БСО'
        ordering = ['-date_at']

    def __str__(self):
        return f'{self.status}'


class StatusBso(models.Model):
    # Статус БСО
    name = models.CharField(max_length=200, verbose_name='Статус БСО')

    class Meta:
        verbose_name = 'Статус БСО'
        verbose_name_plural = 'Статусы БСО'

    def __str__(self):
        return self.name
