from django.contrib import admin
from django.utils.html import format_html, format_html_join
from unfold.admin import ModelAdmin

from src.leads.models import Lead


@admin.register(Lead)
class LeadAdmin(ModelAdmin):
    list_display = (
        'name',
        'phone',
        'email',
        'source',
        'status',
        'is_read',
        'created_at',
    )
    list_filter = ('status', 'source', 'is_read')
    search_fields = ('name', 'phone', 'email')
    readonly_fields = (
        'selected_topics_display',
        'created_at',
        'updated_at',
        'crm_external_id',
        'crm_synced_at',
    )
    list_editable = ('status', 'is_read')
    fields = (
        'name',
        'phone',
        'email',
        'consent',
        'source',
        'source_url',
        'service',
        'selected_topics_display',
        'status',
        'is_read',
        'crm_external_id',
        'crm_synced_at',
        'created_at',
        'updated_at',
    )

    @admin.display(description='Обрані теми')
    def selected_topics_display(self, obj: Lead):
        topics = obj.selected_topics or []
        if not topics:
            return '—'
        return format_html(
            '<ol style="margin:0;padding-left:1.25rem">{}</ol>',
            format_html_join('', '<li>{}</li>', ((topic,) for topic in topics)),
        )
