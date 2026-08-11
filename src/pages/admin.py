from django import forms
from django.contrib import admin
from unfold.admin import ModelAdmin

from src.core.admin_tinymce import TinyMCEAdminMixin
from src.pages.about_hero_validators import ABOUT_HERO_HELP_TEXT
from src.pages.admin_home_block import HomeBlockAdmin
from src.pages.admin_json_forms import SiteSettingsAdminForm
from src.pages.admin_site_content_proxies import register_site_content_section_admins
from src.pages.admin_theme import ActiveThemeAdmin  # noqa: F401 — registers ActiveTheme
from src.pages.models import HomeBlock, HomeHero, Page, SiteSettings


class PageAdminForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = '__all__'

    def clean_hero_image(self):
        image = self.cleaned_data.get('hero_image')
        slug = self.cleaned_data.get('slug') or getattr(self.instance, 'slug', '')
        if image and slug != 'pro-nas':
            raise forms.ValidationError(
                'Фото «Про мене» доступне лише для сторінки зі slug «pro-nas».',
            )
        return image

    def clean_hero_caption(self):
        caption = (self.cleaned_data.get('hero_caption') or '').strip()
        return caption


@admin.register(SiteSettings)
class SiteSettingsAdmin(ModelAdmin):
    form = SiteSettingsAdminForm
    list_display = ('phone', 'email', 'body_font', 'updated_at')
    fieldsets = (
        (
            'Контакти',
            {
                'fields': (
                    'phone',
                    'email',
                    'address',
                    'work_hours',
                    'social_links',
                ),
            },
        ),
        (
            'Заявки',
            {
                'fields': ('lead_notify_email',),
                'description': (
                    'Окремий email для сповіщень про заявки з форм '
                    '(не публічний контакт сайту).'
                ),
            },
        ),
        (
            'Бренд',
            {
                'fields': ('favicon',),
                'description': (
                    'Фавіконка для вкладки браузера та адмінки. '
                    'Формат: PNG / ICO / WEBP, до 512 КБ і 512×512 px.'
                ),
            },
        ),
        (
            'Типографіка',
            {
                'fields': ('body_font',),
                'description': 'Шрифт основного тексту сайту (заголовки лишаються Cormorant Garamond).',
            },
        ),
        (
            'Блог / кейси',
            {
                'fields': (
                    'blog_author_name',
                    'blog_cta_title',
                    'blog_cta_text',
                    'blog_cta_button',
                ),
            },
        ),
        (
            'Карта Google Maps',
            {
                'fields': ('map_embed_url', 'map_lat', 'map_lng'),
                'description': (
                    'Скопіюйте код iframe з Google Maps '
                    '(Поділитися → Вбудувати карту) і вставте в поле нижче. '
                    'Карта з’явиться на сторінці «Контакти».'
                ),
            },
        ),
        (
            'SEO',
            {
                'fields': ('robots_extra',),
                'classes': ('collapse',),
            },
        ),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        from django.http import HttpResponseRedirect
        from django.urls import reverse

        obj, _ = SiteSettings.objects.get_or_create(pk=1)
        return HttpResponseRedirect(
            reverse('admin:pages_sitesettings_change', args=[obj.pk]),
        )

    def save_model(self, request, obj, form, change):
        from django.core.cache import cache

        from src.pages.admin_theme import THEME_CSS_CACHE_KEY

        super().save_model(request, obj, form, change)
        cache.delete(THEME_CSS_CACHE_KEY)


@admin.register(Page)
class PageAdmin(TinyMCEAdminMixin, ModelAdmin):
    form = PageAdminForm
    list_display = ('title', 'slug', 'is_published', 'updated_at')
    list_filter = ('is_published',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'slug')

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            (
                None,
                {
                    'fields': ('title', 'slug', 'body', 'is_published'),
                },
            ),
        ]
        if obj is not None and obj.slug == 'pro-nas':
            fieldsets.append(
                (
                    'Фото «Про мене»',
                    {
                        'fields': ('hero_image', 'hero_image_alt', 'hero_caption'),
                        'description': ABOUT_HERO_HELP_TEXT,
                    },
                ),
            )
        fieldsets.append(
            (
                'SEO',
                {
                    'fields': ('seo_title', 'seo_description', 'seo_h1'),
                    'classes': ('collapse',),
                },
            ),
        )
        return fieldsets


@admin.register(HomeHero)
class HomeHeroAdmin(ModelAdmin):
    """Legacy singleton — пріоритет текстів/фото у CMS «Головна · Hero»."""

    list_display = ('headline', 'is_active', 'updated_at')

    def has_add_permission(self, request):
        return not HomeHero.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(HomeBlock, HomeBlockAdmin)

register_site_content_section_admins()
