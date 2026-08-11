from django.db import models

from src.core.models import TimeStampedModel


class Redirect301(TimeStampedModel):
    old_path = models.CharField('Старий шлях', max_length=255, unique=True)
    new_path = models.CharField('Новий шлях', max_length=255)
    is_active = models.BooleanField('Активний', default=True)

    class Meta:
        db_table = 'seo_redirect_301'
        verbose_name = '301 редірект'
        verbose_name_plural = '301 редіректи'
        ordering = ['old_path']

    def __str__(self) -> str:
        return f'{self.old_path} → {self.new_path}'
