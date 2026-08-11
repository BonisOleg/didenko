"""SiteBlock CMS model."""

from django.db import models

from src.core.models import TimeStampedModel


class SiteBlock(TimeStampedModel):
    class Page(models.TextChoices):
        HOME = 'home', 'Головна'
        SITE = 'site', 'Сайт'
        SERVICES = 'services', 'Послуги'
        CONTACTS = 'contacts', 'Контакти'
        BLOG = 'blog', 'Блог'

    class ContentType(models.TextChoices):
        TEXT = 'text', 'Текст'
        IMAGE = 'image', 'Фото'
        URL = 'url', 'Посилання'

    page = models.CharField('Сторінка', max_length=32, choices=Page.choices)
    key = models.CharField('Ключ', max_length=64)
    label = models.CharField('Підпис', max_length=128)
    content_type = models.CharField(
        'Тип',
        max_length=16,
        choices=ContentType.choices,
        default=ContentType.TEXT,
    )
    text_html = models.TextField('Текст', blank=True, default='')
    image = models.ImageField('Зображення', upload_to='blocks/', blank=True)
    link_url = models.CharField('URL', max_length=512, blank=True, default='')
    link_label = models.CharField('Текст посилання', max_length=128, blank=True, default='')
    sort_order = models.PositiveSmallIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активний', default=True)

    class Meta:
        db_table = 'pages_site_block'
        ordering = ['sort_order', 'key']
        verbose_name = 'Блок контенту'
        verbose_name_plural = 'Блоки контенту'
        constraints = [
            models.UniqueConstraint(
                fields=['page', 'key'],
                name='unique_site_block_page_key',
            ),
        ]

    def __str__(self) -> str:
        return f'{self.page}.{self.key}'

    @property
    def cache_key(self) -> str:
        return f'{self.page}.{self.key}'
