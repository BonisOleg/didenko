"""Форми адмінки з інтуїтивними JSON-списками."""

from django import forms

from src.pages.about_metrics import normalize_metrics
from src.pages.admin_json_widgets import JsonObjectListField, JsonStringListField
from src.pages.admin_site_content_widgets import apply_readable_widget
from src.pages.favicon_validators import validate_favicon_upload
from src.pages.map_embed import MAP_EMBED_HELP_TEXT, normalize_google_maps_embed
from src.pages.models import Page, SiteSettings
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


class PageAdminForm(forms.ModelForm):
    metrics = JsonObjectListField(
        label='Ключові показники',
        add_label='Додати показник',
        help_text=(
            'Число для анімації, суфікс (напр. % або +) і підпис. '
            'Лише для сторінки «Про мене».'
        ),
        item_fields=[
            ('value', 'Число', 'input'),
            ('suffix', 'Суфікс', 'input'),
            ('label', 'Підпис', 'input'),
        ],
    )

    class Meta:
        model = Page
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'metrics':
                continue
            apply_readable_widget(field)

    def clean_hero_image(self):
        image = self.cleaned_data.get('hero_image')
        slug = self.cleaned_data.get('slug') or getattr(self.instance, 'slug', '')
        if image and slug != 'pro-nas':
            raise forms.ValidationError(
                'Фото «Про мене» доступне лише для сторінки зі slug «pro-nas».',
            )
        return image

    def clean_hero_caption(self):
        return (self.cleaned_data.get('hero_caption') or '').strip()

    def clean_metrics(self):
        slug = self.cleaned_data.get('slug') or getattr(self.instance, 'slug', '')
        if slug != 'pro-nas':
            return []
        items = normalize_metrics(self.cleaned_data.get('metrics'))
        raw = self.cleaned_data.get('metrics') or []
        if isinstance(raw, list) and raw and not items:
            raise forms.ValidationError(
                'Кожен показник потребує ціле число та підпис.',
            )
        for row in raw:
            if not isinstance(row, dict):
                continue
            value = str(row.get('value') or '').strip()
            label = str(row.get('label') or '').strip()
            if (value or label or str(row.get('suffix') or '').strip()) and (
                not value.isdigit() or not label
            ):
                raise forms.ValidationError(
                    'Кожен показник потребує ціле число та підпис.',
                )
        return items
