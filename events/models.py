from django.db import models


# Create your models here.


class Events(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    meeting_time = models.DateTimeField(verbose_name='Дата')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, verbose_name='Категория', blank=True)

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'
        ordering = ('-meeting_time',)


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
