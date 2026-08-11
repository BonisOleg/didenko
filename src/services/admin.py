from django.contrib import admin
from unfold.admin import ModelAdmin

from src.core.admin_tinymce import TinyMCEAdminMixin
from src.pages.admin_json_forms import ServiceAdminForm
from src.services.models import ProcessStep, Service


@admin.register(ProcessStep)
class ProcessStepAdmin(ModelAdmin):
    list_display = ('title', 'sort_order', 'is_active')
    list_editable = ('sort_order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'text')
    ordering_field = 'sort_order'


@admin.register(Service)
class ServiceAdmin(TinyMCEAdminMixin, ModelAdmin):
    form = ServiceAdminForm
    list_display = ('title', 'slug', 'icon_key', 'timeline', 'sort_order', 'is_published')
    list_editable = ('sort_order', 'is_published')
    list_filter = ('is_published', 'icon_key')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'slug', 'short_description')
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'title',
                    'slug',
                    'short_description',
                    'icon_key',
                    'sort_order',
                    'is_published',
                    'cta_label',
                ),
            },
        ),
        (
            'Картка та деталі',
            {
                'fields': (
                    'features',
                    'deliverables',
                    'expected_result',
                    'timeline',
                    'body',
                ),
            },
        ),
        (
            'SEO',
            {
                'classes': ('collapse',),
                'fields': ('seo_title', 'seo_description', 'seo_h1'),
            },
        ),
    )
