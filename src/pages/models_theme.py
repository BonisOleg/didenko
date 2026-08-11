"""ActiveTheme — runtime CSS tokens (theme_switcher_skill)."""

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Q

HEX_VALIDATOR = RegexValidator(
    regex=r'^$|^#[0-9A-Fa-f]{6}$',
    message='Колір має бути у форматі #RRGGBB або порожнім',
)


def _hex_field(label: str) -> models.CharField:
    return models.CharField(
        label,
        max_length=7,
        blank=True,
        default='',
        validators=[HEX_VALIDATOR],
        help_text='Hex #RRGGBB. Порожньо = дефолт з tokens.css.',
    )


class ActiveTheme(models.Model):
    """Singleton pk=1 — семантичні кольори без деплою."""

    color_primary = _hex_field('Основний (кнопки / акцент)')
    color_primary_hover = _hex_field('Основний hover')
    color_accent = _hex_field('Акцент (slate)')
    color_surface = _hex_field('Фон сторінки')
    color_text = _hex_field('Основний текст')
    color_footer = _hex_field('Фон футера')
    color_deep = _hex_field('Глибокий steel (заголовки)')
    color_card = _hex_field('Фон карток')

    reset_to_original = models.BooleanField(
        'Повернути до оригіналу',
        default=False,
        help_text='Записує оригінальну бренд-палітру в усі поля.',
    )
    clear_to_tokens = models.BooleanField(
        'Очистити → tokens.css',
        default=False,
        help_text='Обнуляє поля; сайт бере значення з tokens.css.',
    )
    updated_at = models.DateTimeField('Оновлено', auto_now=True)

    TOKEN_MAP = {
        'color_primary': '--color-accent-red',
        'color_primary_hover': '--color-accent-red-hover',
        'color_accent': '--color-slate-blue',
        'color_surface': '--color-bg-light',
        'color_text': '--color-deep-steel',
        'color_footer': '--color-footer-bg',
        'color_deep': '--color-deep-steel',
        'color_card': '--color-card-bg',
    }

    # Locked brand — поточна тема сайту (fog / steel / crimson)
    ORIGINAL_DEFAULTS = {
        'color_primary': '#B50000',
        'color_primary_hover': '#8C0000',
        'color_accent': '#8C9CA3',
        'color_surface': '#EFF2F5',
        'color_text': '#3D4F5C',
        'color_footer': '#2C3842',
        'color_deep': '#3D4F5C',
        'color_card': '#FFFFFF',
    }

    FIELD_DEFAULTS = dict(ORIGINAL_DEFAULTS)

    class Meta:
        db_table = 'pages_active_theme'
        verbose_name = 'Тема сайту'
        verbose_name_plural = 'Тема сайту'
        constraints = [
            models.CheckConstraint(
                condition=Q(pk=1),
                name='pages_active_theme_singleton_id_1',
            ),
        ]

    def __str__(self) -> str:
        return 'Тема сайту'

    def clean(self):
        if self.reset_to_original and self.clear_to_tokens:
            raise ValidationError(
                'Оберіть лише одну дію: «Повернути до оригіналу» або «Очистити».',
            )

    def save(self, *args, **kwargs):
        self.pk = 1
        if self.reset_to_original:
            for field, value in self.ORIGINAL_DEFAULTS.items():
                setattr(self, field, value)
            self.reset_to_original = False
            self.clear_to_tokens = False
        elif self.clear_to_tokens:
            for field in self.TOKEN_MAP:
                setattr(self, field, '')
            self.clear_to_tokens = False
            self.reset_to_original = False
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError('Singleton ActiveTheme не можна видаляти.')

    @classmethod
    def get_solo(cls) -> 'ActiveTheme':
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def build_css(self) -> str:
        lines: list[str] = []
        for field, var in self.TOKEN_MAP.items():
            value = getattr(self, field, '') or ''
            if value:
                lines.append(f'  {var}: {value};')
        # Aliases used by components
        if self.color_primary:
            lines.append(f'  --accent: {self.color_primary};')
            lines.append(f'  --color-brand-blue: {self.color_primary};')
        if self.color_primary_hover:
            lines.append(f'  --color-accent-red-hover: {self.color_primary_hover};')
        if self.color_text or self.color_deep:
            ink = self.color_deep or self.color_text
            lines.append(f'  --ink: {ink};')
            lines.append(f'  --color-primary-dark: {ink};')
        if self.color_surface:
            lines.append(f'  --paper: {self.color_surface};')
            lines.append(f'  --color-cream-bg: {self.color_surface};')
        if self.color_accent:
            lines.append(f'  --accent-soft: {self.color_accent};')
            lines.append(f'  --color-sage-green: {self.color_accent};')
        if self.color_card:
            lines.append(f'  --surface: {self.color_card};')
        # Keep button text readable even if tokens.css is stale/cached.
        lines.append('  --color-white: #FFFFFF;')
        # dedupe while preserving order
        seen: set[str] = set()
        unique: list[str] = []
        for line in lines:
            if line not in seen:
                seen.add(line)
                unique.append(line)
        return ':root {\n' + '\n'.join(unique) + '\n}\n'
