from django.db import models

from src.core.models import TimeStampedModel


class Lead(TimeStampedModel):
    class Source(models.TextChoices):
        HOME = 'home', 'Головна'
        HERO = 'hero', 'Hero'
        SERVICE = 'service', 'Послуга'
        CONTACTS = 'contacts', 'Контакти'
        BLOG = 'blog', 'Блог'

    class Status(models.TextChoices):
        NEW = 'new', 'Новий лід'
        IN_PROGRESS = 'in_progress', 'В обробці'
        CLOSED = 'closed', 'Закрито'
        SPAM = 'spam', 'Спам'

    name = models.CharField('Імʼя', max_length=120)
    phone = models.CharField('Телефон', max_length=30)
    email = models.EmailField('Email')
    consent = models.BooleanField('Згода GDPR', default=False)
    source = models.CharField(
        'Джерело',
        max_length=32,
        choices=Source.choices,
        default=Source.HOME,
    )
    source_url = models.CharField('URL джерела', max_length=512, blank=True, default='')
    service = models.ForeignKey(
        'services.Service',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='leads',
        verbose_name='Послуга',
    )
    selected_topics = models.JSONField(
        'Обрані теми',
        default=list,
        blank=True,
        help_text='Пункти з блоку «Для кого», які обрав користувач.',
    )
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
        db_index=True,
    )
    is_read = models.BooleanField('Прочитано', default=False)
    crm_external_id = models.CharField(
        'CRM ID',
        max_length=64,
        blank=True,
        default='',
    )
    crm_synced_at = models.DateTimeField('CRM sync', null=True, blank=True)

    class Meta:
        db_table = 'leads_lead'
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['is_read']),
        ]

    def __str__(self) -> str:
        return f'{self.name} · {self.phone}'
