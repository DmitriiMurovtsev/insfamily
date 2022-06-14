from django.db import models


class Script(models.Model):
    name = models.CharField(max_length=100, verbose_name='Скрипт', default='Новый скрипт')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Скрипт'
        verbose_name_plural = 'Скрипты'
        ordering = ['name']


class Step(models.Model):
    name = models.CharField(max_length=50, verbose_name='Этап')
    script = models.ForeignKey(Script, verbose_name='Скрипт', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Этап'
        verbose_name_plural = 'Этапы'


class Stage(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    count = models.IntegerField(verbose_name='Порядковый номер')
    text = models.TextField(verbose_name='Содержание')
    step = models.ForeignKey(Step, verbose_name='Шаг', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Шаг'
        verbose_name_plural = 'Шаги'


class Answer(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    text = models.TextField(verbose_name='Содержание')
    stage = models.ManyToManyField(Stage, verbose_name='Шаг', related_name='answer')
    positive = models.BooleanField(verbose_name='Позитивный ответ', default=False)
    neutral = models.BooleanField(verbose_name='Позитивный ответ', default=False)
    negative = models.BooleanField(verbose_name='Позитивный ответ', default=False)
    link = models.BooleanField(verbose_name='Переход к следующему шагу', default=False)

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return self.name
