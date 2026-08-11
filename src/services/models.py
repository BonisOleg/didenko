from django.db import models
from tinymce.models import HTMLField

from src.core.models import SeoFieldsMixin, TimeStampedModel


class Service(SeoFieldsMixin, TimeStampedModel):
    class IconKey(models.TextChoices):
        CONSULT = 'consult', 'Консультація'
        AUDIT = 'audit', 'Аналіз'
        DOCS = 'docs', 'Документи'
        SUPPORT = 'support', 'Супровід'
        DEFENSE = 'defense', 'Захист'
        CREDITORS = 'creditors', 'Кредитори'

    slug = models.SlugField('Slug', max_length=160, unique=True)
    title = models.CharField('Назва', max_length=255)
    short_description = models.CharField(
        'Короткий опис',
        max_length=500,
        blank=True,
        default='',
    )
    body = HTMLField('Опис', blank=True, default='')
    features = models.JSONField(
        'Швидкий чекліст',
        default=list,
        blank=True,
        help_text='Список коротких пунктів для картки (2–3).',
    )
    deliverables = models.JSONField(
        'Що входить у послугу',
        default=list,
        blank=True,
        help_text='Список deliverables для модалки / деталі.',
    )
    expected_result = models.TextField(
        'Очікуваний результат',
        blank=True,
        default='',
    )
    timeline = models.CharField(
        'Терміни виконання',
        max_length=120,
        blank=True,
        default='',
    )
    icon_key = models.CharField(
        'Іконка',
        max_length=32,
        choices=IconKey.choices,
        blank=True,
        default=IconKey.CONSULT,
    )
    sort_order = models.PositiveIntegerField('Порядок', default=0)
    is_published = models.BooleanField('Опубліковано', default=True)
    cta_label = models.CharField('CTA', max_length=120, blank=True, default='Замовити')

    class Meta:
        db_table = 'services_service'
        verbose_name = 'Послуга'
        verbose_name_plural = 'Послуги'
        ordering = ['sort_order', 'id']
        indexes = [
            models.Index(fields=['is_published', 'sort_order']),
        ]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        from django.urls import reverse

        return reverse('services:detail', kwargs={'slug': self.slug})


class ProcessStep(TimeStampedModel):
    """Кроки «Як проходить співпраця» на /posluhy/ — CRUD з видаленням."""

    title = models.CharField('Заголовок', max_length=160)
    text = models.TextField('Опис', blank=True, default='')
    sort_order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активний', default=True)

    class Meta:
        db_table = 'services_process_step'
        verbose_name = 'Крок процесу'
        verbose_name_plural = 'Кроки процесу'
        ordering = ['sort_order', 'id']

    def __str__(self) -> str:
        return self.title
