from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField('Створено', auto_now_add=True)
    updated_at = models.DateTimeField('Оновлено', auto_now=True)

    class Meta:
        abstract = True


class SeoFieldsMixin(models.Model):
    """SEO override — Title / Description / H1 (ТЗ §2.5, §5.2). Без keywords."""

    seo_title = models.CharField('SEO title', max_length=70, blank=True, default='')
    seo_description = models.CharField(
        'SEO description',
        max_length=160,
        blank=True,
        default='',
    )
    seo_h1 = models.CharField('SEO H1', max_length=255, blank=True, default='')

    class Meta:
        abstract = True
