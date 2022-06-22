import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


def get_start_end_date():
    now = datetime.datetime.now()
    date_start = datetime.datetime(now.year, now.month, 1).date()
    next_month = date_start + datetime.timedelta(35)
    date_end = datetime.datetime(next_month.year, next_month.month, 1).date()
    return date_start, date_end


class Client(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    middle_name = models.CharField(max_length=100, verbose_name='Отчество', blank=True)
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    phone = models.CharField(max_length=10, verbose_name='Телефон', blank=True, null=True)
    email = models.EmailField(max_length=100, verbose_name='Почта', blank=True, null=True)
    birthday = models.DateField(verbose_name='Дата рождения', blank=True, null=True)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'


class User(AbstractUser):
    client = models.ManyToManyField(Client, related_name='user', through='Policy', verbose_name='Клиент')
    agent = models.BooleanField(verbose_name='Агент', default=False)
    admin = models.BooleanField(verbose_name='Админ', default=False)
    middle_name = models.CharField(max_length=100, verbose_name='Отчество', blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_user_sp(self):
        date_start, date_end = get_start_end_date()
        sum_sp_all = 0
        sum_sp_22 = 0

        if len(Policy.objects.filter(
                user=self.id, date_registration__lt=date_end, date_registration__gte=date_start)) > 0:

            # сумма всех сборов
            sum_sp_all = sum(policy.sp for policy in Policy.objects.filter(
                user=self.id,
                date_registration__lt=date_end,
                date_registration__gte=date_start))

            # сумма сборов, где входящее КВ больше 22%
            sum_sp_22 = sum(policy.sp for policy in Policy.objects.filter(
                user=self.id,
                date_registration__lt=date_end,
                date_registration__gte=date_start,
                commission__gte=22))

        return [sum_sp_all, sum_sp_22]

    def get_all_sp(self):
        date_start, date_end = get_start_end_date()
        sum_sp_all = 0
        sum_sp_22 = 0

        if len(Policy.objects.filter(date_registration__lt=date_end, date_registration__gte=date_start)) > 0:

            # сумма всех сборов
            sum_sp_all = sum(policy.sp for policy in Policy.objects.filter(
                date_registration__lt=date_end,
                date_registration__gte=date_start))

            # сумма сборов, где входящее КВ больше 22%
            sum_sp_22 = sum(policy.sp for policy in Policy.objects.filter(
                date_registration__lt=date_end,
                date_registration__gte=date_start,
                commission__gte=22))

        return [sum_sp_all, sum_sp_22]


class Type(models.Model):
    name = models.CharField(max_length=50, verbose_name='Тип полиса')

    class Meta:
        verbose_name = 'Тип полиса'
        verbose_name_plural = 'Типы полисов'

    def __str__(self):
        return self.name


class Channel(models.Model):
    name = models.CharField(max_length=50, verbose_name='Канал продаж')

    class Meta:
        verbose_name = 'Канал продаж'
        verbose_name_plural = 'Каналы продаж'

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=100, verbose_name='Страховая компания')

    class Meta:
        verbose_name = 'Страховая компания'
        verbose_name_plural = 'Страховые компании'

    def __str__(self):
        return self.name


class Policy(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='policy', verbose_name='Продавец',
                             null=True)
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING, related_name='policy', verbose_name='Клиент',
                               null=True)
    channel = models.ForeignKey(Channel, on_delete=models.DO_NOTHING, related_name='policy',
                                verbose_name='Канал продаж')
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, related_name='policy',
                                verbose_name='Страховая компания')
    type = models.ForeignKey(Type, related_name='policy', on_delete=models.DO_NOTHING, verbose_name='Тип полиса')
    series = models.CharField(max_length=20, verbose_name='Серия полиса', blank=True)
    number = models.CharField(max_length=30, verbose_name='Номер полиса')
    date_registration = models.DateField(verbose_name='Дата оформления')
    date_start = models.DateField(verbose_name='Дата начала действия')
    date_end = models.DateField(verbose_name='Дата окончания действия')
    commission = models.DecimalField(decimal_places=2, max_digits=8, verbose_name='КВ в %')
    sp = models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Страховая премия')
    status = models.CharField(max_length=30, verbose_name='Статус полиса', default='newbiz')
    bank = models.CharField(max_length=30, verbose_name='Банк', blank=True, null=True)
    accept = models.BooleanField(verbose_name='Проведен', default=False)
    type_pay = models.BooleanField(verbose_name='Наличные', default=False)
    credit = models.BooleanField(verbose_name='Кредитное ТС', default=False)
    sale_report = models.ForeignKey('SaleReport', on_delete=models.DO_NOTHING, verbose_name='АКТ', blank=True,
                                    null=True)

    class Meta:
        verbose_name = 'Полис'
        verbose_name_plural = 'Полисы'
        ordering = ['-date_registration']

    def __str__(self):
        return f'{self.series} {self.number} {self.company}'


class MortgagePolicy(models.Model):
    date_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    date_end = models.DateField(verbose_name='Дата окончания полиса')
    user = models.ForeignKey(User, verbose_name='Менеджер', on_delete=models.DO_NOTHING)
    client = models.ForeignKey(Client, verbose_name='Клиент', on_delete=models.DO_NOTHING,
                               related_name='mortgage_policy', null=True)
    bank = models.ForeignKey('Bank', verbose_name='Банк', related_name='bank', on_delete=models.DO_NOTHING)
    type_mortgage = models.CharField(max_length=10, verbose_name='Тип ипотечного полиса', default='all')

    class Meta:
        verbose_name = 'Ипотечный полис'
        verbose_name_plural = 'Ипотечный полис'
        ordering = ['-date_end']

    def __str__(self):
        return f'{self.bank} {self.date_end}'


class Bank(models.Model):
    name = models.CharField(max_length=30, verbose_name='Банк')

    class Meta:
        verbose_name = 'Банк'
        verbose_name_plural = 'Банки'

    def __str__(self):
        return f'{self.name}'


class Commission(models.Model):
    date_start = models.DateField(verbose_name='Дата начала действия')
    channel = models.ForeignKey(Channel, on_delete=models.DO_NOTHING, verbose_name='Канал продаж')
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, verbose_name='Компания')
    type = models.ForeignKey(Type, on_delete=models.DO_NOTHING, verbose_name='Тип полиса', default='')
    bank = models.ForeignKey(Bank, on_delete=models.DO_NOTHING, verbose_name='Банк', null=True, default='')
    value = models.DecimalField(verbose_name='КВ', decimal_places=2, max_digits=8)

    class Meta:
        verbose_name = 'Входящее КВ'
        verbose_name_plural = 'Входящее КВ'
        ordering = ['-date_start']

    def __str__(self):
        return f'{self.channel} с {self.date_start}'


class Expenses(models.Model):
    # расходы
    name = models.CharField(max_length=200, verbose_name='Наименование')
    date_expenses = models.DateField(verbose_name='Дата расхода')
    value = models.DecimalField(verbose_name='Сумма расходов', decimal_places=2, max_digits=8)
    salary = models.BooleanField(verbose_name='Зарплата', default=False)
    sale_report = models.ForeignKey('SaleReport', on_delete=models.DO_NOTHING, verbose_name='АКТ', blank=True,
                                    null=True)

    class Meta:
        verbose_name = 'Расход'
        verbose_name_plural = 'Расходы'
        ordering = ['-date_expenses']

    def __str__(self):
        return self.name


class SaleReport(models.Model):
    # итоговый акт проведённых полисов и расходов
    name = models.CharField(max_length=50, verbose_name='Наименование')
    date_create = models.DateField(auto_now=True, verbose_name='Дата создания акта')
