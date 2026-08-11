from django.db import models
from tinymce.models import HTMLField

from src.core.models import SeoFieldsMixin, TimeStampedModel
from src.pages.about_hero_validators import (
    ABOUT_HERO_HELP_TEXT,
    validate_about_hero_image,
)
from src.pages.favicon_validators import validate_favicon_upload


class SiteSettings(TimeStampedModel):
    class BodyFont(models.TextChoices):
        INTER = 'inter', 'Inter'
        PLUS_JAKARTA = 'plus_jakarta', 'Plus Jakarta Sans'
        SYSTEM = 'system', 'Системний'

    phone = models.CharField('Телефон', max_length=32, blank=True, default='')
    email = models.EmailField('Email', blank=True, default='')
    lead_notify_email = models.EmailField(
        'Email для заявок',
        blank=True,
        default='',
        help_text=(
            'Куди надсилати заявки з форм. Якщо порожньо — береться '
            'ADMIN_NOTIFY_EMAIL з оточення.'
        ),
    )
    favicon = models.ImageField(
        'Фавіконка',
        upload_to='brand/favicon/',
        blank=True,
        null=True,
        validators=[validate_favicon_upload],
        help_text=(
            'PNG, ICO або WEBP. Максимум 512 КБ і 512×512 px. '
            'Якщо порожньо — використовується стандартна іконка.'
        ),
    )
    address = models.TextField('Адреса', blank=True, default='')
    work_hours = models.CharField(
        'Графік роботи',
        max_length=120,
        blank=True,
        default='пн–пт з 9:00 до 18:00',
    )
    map_lat = models.DecimalField(
        'Широта',
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )
    map_lng = models.DecimalField(
        'Довгота',
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )
    map_embed_url = models.URLField(
        'Embed карти',
        max_length=2048,
        blank=True,
        default='',
        help_text=(
            'Вставте код iframe з Google Maps (Поділитися → Вбудувати карту) '
            'або прямий embed URL.'
        ),
    )
    social_links = models.JSONField('Соцмережі', default=list, blank=True)
    robots_extra = models.TextField('Доп. robots.txt', blank=True, default='')
    body_font = models.CharField(
        'Шрифт тексту',
        max_length=32,
        choices=BodyFont.choices,
        default=BodyFont.INTER,
    )
    blog_cta_title = models.CharField(
        'Блог CTA заголовок',
        max_length=120,
        default='Потрібна консультація?',
        blank=True,
    )
    blog_cta_text = models.TextField(
        'Блог CTA текст',
        blank=True,
        default=(
            'Оціню вашу ситуацію та запропоную оптимальний правовий шлях '
            'у межах Кодексу України з процедур банкрутства.'
        ),
    )
    blog_cta_button = models.CharField(
        'Блог CTA кнопка',
        max_length=80,
        default='Залишити заявку',
        blank=True,
    )
    blog_author_name = models.CharField(
        'Автор у блозі',
        max_length=120,
        default='Діденко Валерія Валеріївна',
        blank=True,
    )

    class Meta:
        db_table = 'pages_site_settings'
        verbose_name = 'Налаштування сайту'
        verbose_name_plural = 'Налаштування сайту'

    def __str__(self) -> str:
        return 'Налаштування сайту'

    @property
    def body_font_stack(self) -> str:
        stacks = {
            self.BodyFont.INTER: '"Inter", system-ui, -apple-system, sans-serif',
            self.BodyFont.PLUS_JAKARTA: (
                '"Plus Jakarta Sans", system-ui, -apple-system, sans-serif'
            ),
            self.BodyFont.SYSTEM: (
                'system-ui, -apple-system, "Segoe UI", Roboto, sans-serif'
            ),
        }
        return stacks.get(self.body_font, stacks[self.BodyFont.INTER])

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls) -> 'SiteSettings':
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Page(SeoFieldsMixin, TimeStampedModel):
    slug = models.SlugField('Slug', max_length=160, unique=True)
    title = models.CharField('Заголовок', max_length=255)
    body = HTMLField('Контент', blank=True, default='')
    is_published = models.BooleanField('Опубліковано', default=True)
    hero_image = models.ImageField(
        'Фото «Про мене»',
        upload_to='about/',
        blank=True,
        null=True,
        validators=[validate_about_hero_image],
        help_text=ABOUT_HERO_HELP_TEXT,
    )
    hero_image_alt = models.CharField(
        'Alt фото',
        max_length=255,
        blank=True,
        default='',
        help_text='Короткий опис фото для доступності. Якщо порожньо — береться H1.',
    )
    hero_caption = models.CharField(
        'Підпис на фото',
        max_length=160,
        blank=True,
        default='',
        help_text=(
            'Текст на склі поверх фото. Очистіть поле, щоб прибрати підпис.'
        ),
    )
    metrics = models.JSONField(
        'Ключові показники',
        default=list,
        blank=True,
        help_text=(
            'Лише для «Про мене» (pro-nas). Список: число, суфікс (% / +), підпис.'
        ),
    )

    class Meta:
        db_table = 'pages_page'
        verbose_name = 'Інфо-сторінка'
        verbose_name_plural = 'Інфо-сторінки'
        ordering = ['title']
        indexes = [
            models.Index(fields=['is_published', 'slug']),
        ]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        from django.urls import reverse

        return reverse('pages:page_detail', kwargs={'slug': self.slug})

    def normalized_metrics(self) -> list[dict[str, str]]:
        from src.pages.about_metrics import normalize_metrics

        return normalize_metrics(self.metrics)


class HomeHero(TimeStampedModel):
    headline = models.CharField('H1', max_length=255)
    subheadline = models.TextField('Підзаголовок', blank=True, default='')
    image = models.ImageField(
        'Зображення 21:9',
        upload_to='hero/',
        blank=True,
        null=True,
    )
    image_alt = models.CharField('Alt', max_length=255, blank=True, default='')
    cta_label = models.CharField('CTA текст', max_length=120, default='Залишити заявку')
    cta_target = models.CharField(
        'CTA ціль',
        max_length=64,
        default='#lead-form',
        help_text='#lead-form або modal:lead',
    )
    is_active = models.BooleanField('Активний', default=True)

    class Meta:
        db_table = 'pages_home_hero'
        verbose_name = 'Hero головної'
        verbose_name_plural = 'Hero головної'

    def __str__(self) -> str:
        return self.headline[:60]

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls) -> 'HomeHero':
        obj, _ = cls.objects.get_or_create(
            pk=1,
            defaults={
                'headline': 'Банкрутство фізичних осіб під ключ',
                'subheadline': (
                    'Законне списання боргів відповідно до Кодексу України '
                    'з процедур банкрутства.'
                ),
            },
        )
        return obj


class HomeBlock(TimeStampedModel):
    class BlockType(models.TextChoices):
        SERVICES_TEASER = 'services_teaser', 'Превʼю послуг'
        ADVANTAGES = 'advantages', 'Чому звертаються'
        AUDIENCE = 'audience', 'Для кого'
        BLOG_TEASER = 'blog_teaser', 'Превʼю блогу'
        LEAD_FORM = 'lead_form', 'Форма заявки'

    block_type = models.CharField(
        'Тип',
        max_length=32,
        choices=BlockType.choices,
    )
    title = models.CharField('Заголовок секції', max_length=255, blank=True, default='')
    payload = models.JSONField('Payload', default=dict, blank=True)
    sort_order = models.PositiveIntegerField('Порядок', default=0)
    is_visible = models.BooleanField('Видимий', default=True)

    class Meta:
        db_table = 'pages_home_block'
        verbose_name = 'Блок головної'
        verbose_name_plural = 'Блоки головної'
        ordering = ['sort_order', 'id']
        indexes = [
            models.Index(fields=['is_visible', 'sort_order']),
        ]

    def __str__(self) -> str:
        return f'{self.get_block_type_display()} ({self.sort_order})'


# CMS / theme (import for migrations discovery)
from src.pages.models_siteblock import SiteBlock  # noqa: E402,F401
from src.pages.models_theme import ActiveTheme  # noqa: E402,F401
from src.pages.models_proxies import (  # noqa: E402,F401
    BlogPageSettings,
    ContactsPageSettings,
    HomeAdvantagesSettings,
    HomeAudienceSettings,
    HomeBlogSettings,
    HomeHeroSettings,
    HomeLeadSettings,
    HomeServicesSettings,
    ServicesPageSettings,
    SiteBrandSettings,
    SiteFooterSettings,
    SiteFormsSettings,
    SiteNavigationSettings,
)
