"""Форми адмінки з інтуїтивними JSON-списками."""

from django import forms

from src.pages.admin_json_widgets import JsonObjectListField, JsonStringListField
from src.pages.admin_site_content_widgets import apply_readable_widget
from src.pages.favicon_validators import validate_favicon_upload
from src.pages.map_embed import MAP_EMBED_HELP_TEXT, normalize_google_maps_embed
from src.pages.models import SiteSettings
from src.services.models import Service


class SiteSettingsAdminForm(forms.ModelForm):
    social_links = JsonObjectListField(
        label='Соцмережі',
        add_label='Додати соцмережу',
        item_fields=[
            ('label', 'Назва', 'input'),
            ('url', 'Посилання', 'input'),
        ],
    )
    map_embed_url = forms.CharField(
        label='Карта Google Maps',
        required=False,
        help_text=MAP_EMBED_HELP_TEXT,
        widget=forms.Textarea(attrs={'rows': 4}),
    )

    class Meta:
        model = SiteSettings
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'social_links':
                continue
            apply_readable_widget(field)

    def clean_favicon(self):
        from django.core.files.uploadedfile import UploadedFile

        favicon = self.cleaned_data.get('favicon')
        if isinstance(favicon, UploadedFile):
            validate_favicon_upload(favicon)
        return favicon

    def clean_map_embed_url(self):
        return normalize_google_maps_embed(
            self.cleaned_data.get('map_embed_url') or '',
        )


class ServiceAdminForm(forms.ModelForm):
    features = JsonStringListField(
        label='Швидкий чекліст',
        item_label='Пункт',
        add_label='Додати пункт',
        help_text='Короткі пункти для картки послуги (зазвичай 2–3).',
    )
    deliverables = JsonStringListField(
        label='Що входить у послугу',
        item_label='Пункт',
        add_label='Додати пункт',
        help_text='Список для модалки та сторінки деталі.',
    )

    class Meta:
        model = Service
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name in {'features', 'deliverables'}:
                continue
            apply_readable_widget(field)
