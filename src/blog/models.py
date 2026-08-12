from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField

from src.core.models import SeoFieldsMixin, TimeStampedModel


class Category(TimeStampedModel):
    slug = models.SlugField('Slug', max_length=160, unique=True)
    title = models.CharField('Назва', max_length=255)
    sort_order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активна', default=True)

    class Meta:
        db_table = 'blog_category'
        verbose_name = 'Категорія блогу'
        verbose_name_plural = 'Категорії блогу'
        ordering = ['sort_order', 'id']

    def __str__(self) -> str:
        return self.title


class Post(SeoFieldsMixin, TimeStampedModel):
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name='Категорія',
    )
    slug = models.SlugField('Slug', max_length=160, unique=True)
    title = models.CharField('Заголовок', max_length=255)
    excerpt = models.CharField('Анонс', max_length=500, blank=True, default='')
    body = HTMLField('Контент', blank=True, default='')
    cover_image = models.ImageField(
        'Обкладинка',
        upload_to='blog/',
        blank=True,
        null=True,
        help_text=(
            'Формат: JPG, PNG або WebP. Рекомендований розмір 960×540 px '
            '(співвідношення 16:9). Мінімум 640×360 px. Файл до 1 МБ. '
            'Інакше зображення обріжеться або розтягне верстку.'
        ),
    )
    cover_alt = models.CharField('Alt обкладинки', max_length=255, blank=True, default='')
    is_published = models.BooleanField('Опубліковано', default=False)
    is_featured = models.BooleanField('Головний кейс', default=False)
    published_at = models.DateTimeField('Дата публікації', null=True, blank=True)

    class Meta:
        db_table = 'blog_post'
        verbose_name = 'Запис блогу'
        verbose_name_plural = 'Записи блогу'
        ordering = ['-published_at', '-id']
        indexes = [
            models.Index(fields=['is_published', '-published_at']),
            models.Index(fields=['category', '-published_at']),
            models.Index(fields=['is_featured', '-published_at']),
        ]

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if self.is_published and self.published_at is None:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)
        if self.is_featured and self.pk:
            (
                Post.objects.filter(is_featured=True)
                .exclude(pk=self.pk)
                .update(is_featured=False)
            )

    def get_absolute_url(self) -> str:
        from django.urls import reverse

        return reverse('blog:detail', kwargs={'slug': self.slug})

    @property
    def cover_url(self) -> str:
        """URL обкладинки: media, інакше static/img/blog/{slug}.webp."""
        from pathlib import Path

        from django.conf import settings
        from django.templatetags.static import static

        if self.cover_image:
            try:
                if Path(self.cover_image.path).is_file():
                    return self.cover_image.url
            except (NotImplementedError, ValueError, OSError):
                return self.cover_image.url

        static_rel = f'img/blog/{self.slug}.webp'
        static_path = Path(settings.BASE_DIR) / 'static' / static_rel
        if static_path.is_file():
            return static(static_rel)
        # Після collectstatic у контейнері джерело може бути лише в STATIC_ROOT
        collected = Path(settings.STATIC_ROOT) / static_rel
        if collected.is_file():
            return static(static_rel)
        return ''

    @property
    def read_time_minutes(self) -> int:
        from django.utils.html import strip_tags

        text = f'{self.excerpt} {strip_tags(self.body or "")}'
        words = len(text.split())
        return max(1, round(words / 180)) if words else 1

    @property
    def published_label(self) -> str:
        if not self.published_at:
            return ''
        months = (
            '',
            'Січня',
            'Лютого',
            'Березня',
            'Квітня',
            'Травня',
            'Червня',
            'Липня',
            'Серпня',
            'Вересня',
            'Жовтня',
            'Листопада',
            'Грудня',
        )
        local = timezone.localtime(self.published_at)
        return f'{local.day:02d} {months[local.month]}, {local.year}'
