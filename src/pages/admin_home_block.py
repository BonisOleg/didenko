"""Адмінка HomeBlock: форма під тип блоку без сирого JSON."""

from __future__ import annotations

from django import forms
from django.conf import settings
from django.core.cache import cache
from unfold.admin import ModelAdmin

from src.pages.admin_json_widgets import JsonObjectListField, JsonStringListField
from src.pages.admin_site_content_widgets import CmsAdminTextInputWidget, CmsAdminTextareaWidget
from src.pages.models import HomeBlock


def _site_block_text(page: str, key: str) -> str:
    from src.pages.models_siteblock import SiteBlock

    block = SiteBlock.objects.filter(page=page, key=key).only('text_html').first()
    return (block.text_html if block else '') or ''


def _sync_site_block_text(page: str, key: str, text: str, label: str) -> None:
    from src.pages.models_siteblock import SiteBlock

    block, _ = SiteBlock.objects.get_or_create(
        page=page,
        key=key,
        defaults={
            'label': label,
            'text_html': text,
            'content_type': SiteBlock.ContentType.TEXT,
            'is_active': True,
        },
    )
    if block.text_html != text or block.label != label:
        block.text_html = text
        block.label = label
        block.save(update_fields=['text_html', 'label'])
    cache.delete(getattr(settings, 'SITE_BLOCKS_CACHE_KEY', 'didenko_site_blocks_v1'))


class HomeBlockAdminForm(forms.ModelForm):
    payload_intro = forms.CharField(
        label='Вступ',
        required=False,
        widget=CmsAdminTextareaWidget(attrs={'rows': 3}),
        help_text='Текст під заголовком секції (синхронізується з CMS).',
    )
    payload_items_strings = JsonStringListField(
        label='Список пунктів',
        item_label='Пункт',
        add_label='Додати пункт',
    )
    payload_items_cards = JsonObjectListField(
        label='Картки переваг',
        add_label='Додати картку',
        item_fields=[
            ('title', 'Заголовок', 'input'),
            ('text', 'Опис', 'textarea'),
        ],
    )
    payload_limit = forms.IntegerField(
        label='Скільки показувати',
        required=False,
        min_value=1,
        max_value=24,
        widget=CmsAdminTextInputWidget(attrs={'type': 'number', 'min': 1, 'max': 24}),
    )
    payload_anchor = forms.CharField(
        label='Якір секції (id)',
        required=False,
        max_length=64,
        widget=CmsAdminTextInputWidget(),
        help_text='Наприклад: lead-form — для посилань #lead-form',
    )
    payload_heading = forms.CharField(
        label='Заголовок у payload',
        required=False,
        max_length=255,
        widget=CmsAdminTextInputWidget(),
    )

    class Meta:
        model = HomeBlock
        fields = (
            'block_type',
            'title',
            'sort_order',
            'is_visible',
        )
        widgets = {
            'title': CmsAdminTextInputWidget(),
            'sort_order': CmsAdminTextInputWidget(attrs={'type': 'number', 'min': 0}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        payload = {}
        if self.instance and self.instance.pk:
            payload = self.instance.payload or {}
        btype = (
            self.data.get('block_type')
            if self.is_bound
            else (self.instance.block_type if self.instance.pk else '')
        )

        if btype == HomeBlock.BlockType.AUDIENCE:
            cms_intro = _site_block_text('home', 'audience_intro')
            self.fields['payload_intro'].initial = cms_intro or payload.get('intro', '')
            self.fields['payload_items_strings'].initial = payload.get('items') or ['']
        elif btype == HomeBlock.BlockType.ADVANTAGES:
            cms_intro = _site_block_text('home', 'advantages_intro')
            self.fields['payload_intro'].initial = cms_intro or payload.get('intro', '')
            self.fields['payload_items_cards'].initial = payload.get('items') or []
        elif btype == HomeBlock.BlockType.SERVICES_TEASER:
            self.fields['payload_limit'].initial = int(payload.get('limit') or 6)
        elif btype == HomeBlock.BlockType.BLOG_TEASER:
            self.fields['payload_limit'].initial = int(payload.get('limit') or 3)
        elif btype == HomeBlock.BlockType.LEAD_FORM:
            self.fields['payload_heading'].initial = payload.get('heading', '')
            self.fields['payload_anchor'].initial = payload.get('anchor') or 'lead-form'

    def clean(self):
        cleaned = super().clean()
        btype = cleaned.get('block_type')
        payload: dict = {}

        if btype == HomeBlock.BlockType.AUDIENCE:
            payload = {
                'intro': (cleaned.get('payload_intro') or '').strip(),
                'items': cleaned.get('payload_items_strings') or [],
            }
        elif btype == HomeBlock.BlockType.ADVANTAGES:
            payload = {
                'intro': (cleaned.get('payload_intro') or '').strip(),
                'items': cleaned.get('payload_items_cards') or [],
            }
        elif btype == HomeBlock.BlockType.SERVICES_TEASER:
            payload = {'limit': cleaned.get('payload_limit') or 6}
        elif btype == HomeBlock.BlockType.BLOG_TEASER:
            payload = {'limit': cleaned.get('payload_limit') or 3}
        elif btype == HomeBlock.BlockType.LEAD_FORM:
            payload = {
                'heading': (cleaned.get('payload_heading') or '').strip(),
                'anchor': (cleaned.get('payload_anchor') or 'lead-form').strip() or 'lead-form',
            }

        cleaned['_payload'] = payload
        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.payload = self.cleaned_data.get('_payload') or {}
        if commit:
            instance.save()
        return instance

    def sync_cms_intro(self, instance: HomeBlock) -> None:
        intro = (instance.payload or {}).get('intro')
        if intro is None:
            return
        if instance.block_type == HomeBlock.BlockType.AUDIENCE:
            _sync_site_block_text('home', 'audience_intro', intro, 'Вступ')
        elif instance.block_type == HomeBlock.BlockType.ADVANTAGES:
            _sync_site_block_text('home', 'advantages_intro', intro, 'Вступ')


class HomeBlockAdmin(ModelAdmin):
    form = HomeBlockAdminForm
    list_display = ('block_type', 'title', 'sort_order', 'is_visible')
    list_editable = ('sort_order', 'is_visible')
    list_filter = ('block_type', 'is_visible')
    ordering_field = 'sort_order'

    class Media:
        css = {'all': ('css/admin/json_list_widget.css', 'css/admin/home_block_form.css')}
        js = ('js/admin/json_list_widget.js', 'js/admin/home_block_form.js')

    def get_fieldsets(self, request, obj=None):
        return (
            (
                None,
                {
                    'fields': ('block_type', 'title', 'sort_order', 'is_visible'),
                },
            ),
            (
                'Контент секції',
                {
                    'fields': (
                        'payload_intro',
                        'payload_items_strings',
                        'payload_items_cards',
                        'payload_limit',
                        'payload_heading',
                        'payload_anchor',
                    ),
                    'description': (
                        'Поля змінюються залежно від типу блоку. '
                        'Сирий JSON більше не потрібен.'
                    ),
                },
            ),
        )

    def get_changelist_form(self, request, **kwargs):
        return forms.modelform_factory(
            HomeBlock,
            fields=['sort_order', 'is_visible'],
        )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if hasattr(form, 'sync_cms_intro'):
            form.sync_cms_intro(obj)
