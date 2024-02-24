from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


# Create your models here.


class Events(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    meeting_time = models.DateTimeField(verbose_name='Дата')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, verbose_name='Категория', blank=True)
    users = models.ManyToManyField(User, blank=True, related_name="events", verbose_name="Пользователи")

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'
        ordering = ('meeting_time',)

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title
