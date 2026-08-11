"""Theme admin + CSS view helpers."""

from django import forms
from django.contrib import admin
from django.core.cache import cache
from django.http import HttpResponse
from django.urls import reverse
from django.utils.html import format_html
from django.views.decorators.http import require_GET
from unfold.admin import ModelAdmin

from src.pages.admin_utils import SingletonModelAdminMixin
from src.pages.models_theme import ActiveTheme

THEME_CSS_CACHE_KEY = 'didenko_theme_css_v1'


class ActiveThemeAdminForm(forms.ModelForm):
    class Meta:
        model = ActiveTheme
        fields = '__all__'
        widgets = {
            field: forms.TextInput(attrs={'type': 'color'})
            for field in ActiveTheme.TOKEN_MAP
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, default in ActiveTheme.FIELD_DEFAULTS.items():
            if field_name in self.fields:
                current = getattr(self.instance, field_name, '') if self.instance else ''
                if not current:
                    self.fields[field_name].widget.attrs['value'] = default
                    self.fields[field_name].initial = default


@admin.register(ActiveTheme)
class ActiveThemeAdmin(SingletonModelAdminMixin, ModelAdmin):
    form = ActiveThemeAdminForm
    change_url_name = 'admin:pages_activetheme_change'
    readonly_fields = ('preview_link', 'updated_at')
    fieldsets = (
        (
            'Бренд',
            {
                'fields': (
                    'color_primary',
                    'color_primary_hover',
                    'color_accent',
                    'color_deep',
                ),
            },
        ),
        (
            'Поверхні',
            {
                'fields': ('color_surface', 'color_card', 'color_text', 'color_footer'),
            },
        ),
        (
            'Скидання',
            {
                'fields': ('reset_to_original', 'clear_to_tokens'),
                'description': (
                    '«Повернути до оригіналу» — поточна бренд-палітра сайту. '
                    '«Очистити» — порожні поля → tokens.css.'
                ),
            },
        ),
        ('Службове', {'fields': ('preview_link', 'updated_at')}),
    )

    def preview_link(self, obj):
        return format_html(
            '<a href="{}" target="_blank" rel="noopener">Відкрити сайт</a> · '
            '<a href="{}" target="_blank" rel="noopener">theme.css</a>',
            '/',
            reverse('theme_css'),
        )

    preview_link.short_description = 'Превʼю'

    def has_add_permission(self, request):
        return not ActiveTheme.objects.exists()

    def changelist_view(self, request, extra_context=None):
        from django.http import HttpResponseRedirect
        from django.urls import reverse

        obj, _ = ActiveTheme.objects.get_or_create(pk=1)
        return HttpResponseRedirect(
            reverse('admin:pages_activetheme_change', args=[obj.pk]),
        )

    def save_model(self, request, obj, form, change):
        obj.full_clean()
        super().save_model(request, obj, form, change)
        cache.delete(THEME_CSS_CACHE_KEY)


@require_GET
def theme_css(request):
    css = cache.get(THEME_CSS_CACHE_KEY)
    if css is None:
        theme = ActiveTheme.get_solo()
        parts = [theme.build_css().rstrip()]
        try:
            from src.pages.models import SiteSettings

            settings_obj = SiteSettings.load()
            stack = settings_obj.body_font_stack
            if stack:
                parts.append(f':root {{ --font-body: {stack}; }}')
        except Exception:
            pass
        css = '\n'.join(parts) + '\n'
        cache.set(THEME_CSS_CACHE_KEY, css, 3600)
    response = HttpResponse(css, content_type='text/css; charset=utf-8')
    response['Cache-Control'] = 'public, max-age=300'
    return response
