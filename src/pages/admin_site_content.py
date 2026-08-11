"""Форма та view CMS-секцій."""

from django import forms
from django.conf import settings
from django.contrib import admin, messages
from django.contrib.admin.utils import unquote
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from unfold.widgets import UnfoldAdminFileFieldWidget, UnfoldBooleanWidget

from src.pages.admin_site_content_widgets import CmsAdminTextInputWidget, CmsAdminTextareaWidget
from src.pages.block_defaults import (
    BLOCK_CONTENT_TYPES,
    BLOCK_FIELD_HELP,
    INLINE_KEYS,
    MULTILINE_KEYS,
    default_for_key,
    is_visibility_key,
)
from src.pages.models_siteblock import SiteBlock
from src.pages.site_content_registry import (
    get_section,
    iter_section_blocks,
    label_for_block,
)


def block_field_name(page: str, key: str, suffix: str) -> str:
    return f'block__{page}__{key}__{suffix}'


def load_section_blocks(section) -> dict[tuple[str, str], SiteBlock]:
    blocks: dict[tuple[str, str], SiteBlock] = {}
    for page, key in iter_section_blocks(section):
        default_text = default_for_key(page, key)
        content_type = BLOCK_CONTENT_TYPES.get((page, key), 'text')
        block, created = SiteBlock.objects.get_or_create(
            page=page,
            key=key,
            defaults={
                'label': label_for_block(page, key),
                'text_html': default_text,
                'content_type': content_type,
                'sort_order': len(blocks) + 1,
                'is_active': True,
            },
        )
        if not created:
            update_fields: list[str] = []
            registry_label = label_for_block(page, key)
            if block.content_type != content_type:
                block.content_type = content_type
                update_fields.append('content_type')
            if block.label != registry_label:
                block.label = registry_label
                update_fields.append('label')
            if update_fields:
                block.save(update_fields=update_fields)
        blocks[(page, key)] = block
    return blocks


class SitePageContentForm(forms.Form):
    section_visible = forms.BooleanField(
        label='Показувати секцію на сайті',
        required=False,
        widget=UnfoldBooleanWidget,
    )

    def __init__(self, *args, section=None, blocks=None, **kwargs):
        self.section = section
        self.blocks = blocks or {}
        super().__init__(*args, **kwargs)

        if section and section.visibility_key:
            visibility_block = blocks.get((section.page_slug, section.visibility_key))
            if visibility_block:
                self.fields['section_visible'].initial = visibility_block.text_html not in {
                    '0',
                    'false',
                    'False',
                    '',
                }

        for page, key in section.blocks if section else ():
            block = blocks.get((page, key))
            if not block:
                continue
            field_key = (page, key)
            help_text = BLOCK_FIELD_HELP.get(field_key, '')

            if is_visibility_key(key):
                self.fields[block_field_name(page, key, 'visible')] = forms.BooleanField(
                    label=label_for_block(page, key),
                    required=False,
                    initial=block.text_html not in {'0', 'false', 'False', ''},
                    widget=UnfoldBooleanWidget,
                    help_text=help_text,
                )
                continue

            if block.content_type == SiteBlock.ContentType.IMAGE:
                self.fields[block_field_name(page, key, 'image')] = forms.ImageField(
                    label=label_for_block(page, key),
                    required=False,
                    widget=UnfoldAdminFileFieldWidget,
                    initial=block.image if block.image else None,
                    help_text=help_text,
                )
                continue

            if field_key in INLINE_KEYS:
                widget = CmsAdminTextInputWidget()
                rows = None
            elif field_key in MULTILINE_KEYS:
                widget = CmsAdminTextareaWidget(attrs={'rows': 4})
                rows = 4
            else:
                widget = CmsAdminTextareaWidget(attrs={'rows': 2})
                rows = 2

            self.fields[block_field_name(page, key, 'text_html')] = forms.CharField(
                label=label_for_block(page, key),
                required=False,
                initial=block.text_html,
                widget=widget,
            )
            if rows:
                self.fields[block_field_name(page, key, 'text_html')].widget.attrs['rows'] = rows

    def save(self) -> None:
        section = self.section
        if section is None:
            return

        if section.visibility_key:
            visibility_block = self.blocks.get((section.page_slug, section.visibility_key))
            if visibility_block:
                visibility_block.text_html = (
                    '1' if self.cleaned_data.get('section_visible') else '0'
                )
                visibility_block.save(update_fields=['text_html'])

        for page, key in section.blocks:
            block = self.blocks.get((page, key))
            if not block:
                continue

            if is_visibility_key(key):
                field_name = block_field_name(page, key, 'visible')
                block.text_html = '1' if self.cleaned_data.get(field_name) else '0'
                block.save(update_fields=['text_html'])
                continue

            if block.content_type == SiteBlock.ContentType.IMAGE:
                image = self.cleaned_data.get(block_field_name(page, key, 'image'))
                if image is False:
                    if block.image:
                        block.image.delete(save=False)
                    block.image = None
                    block.save(update_fields=['image'])
                elif image:
                    block.image = image
                    block.save(update_fields=['image'])
                continue

            text_field = block_field_name(page, key, 'text_html')
            block.text_html = self.cleaned_data.get(text_field, '')
            block.save(update_fields=['text_html'])

        cache.delete(getattr(settings, 'SITE_BLOCKS_CACHE_KEY', 'didenko_site_blocks_v1'))


def site_content_section_view(request, page_slug, section_slug, model_admin=None):
    section = get_section(page_slug, section_slug)
    if section is None:
        messages.error(request, 'Секцію не знайдено.')
        return HttpResponseRedirect(reverse('admin:index'))

    blocks = load_section_blocks(section)
    opts = model_admin.model._meta if model_admin else SiteBlock._meta

    if request.method == 'POST':
        form = SitePageContentForm(
            request.POST,
            request.FILES,
            section=section,
            blocks=blocks,
        )
        if form.is_valid():
            form.save()
            messages.success(request, 'Зміни збережено.')
            return HttpResponseRedirect(request.path)
        messages.error(request, 'Перевірте форму — є помилки.')
    else:
        form = SitePageContentForm(section=section, blocks=blocks)

    context = {
        **admin.site.each_context(request),
        'form': form,
        'section': section,
        'grouped_bound_fields': _build_grouped_bound_fields(form, section, section.page_slug),
        'image_previews': _image_previews(blocks),
        'opts': opts,
        'app_label': opts.app_label,
        'model_name': opts.model_name,
        'title': section.title,
        'preview_url': section.preview_url,
        'description': section.description,
        'has_view_permission': True,
        'has_change_permission': True,
        'original': None,
        'object_id': unquote('1'),
    }
    return render(request, 'admin/pages/site_content_page.html', context)


def _build_grouped_bound_fields(form, section, page_slug: str):
    grouped_fields: list[tuple[str, list[str]]] = []
    if section.field_groups:
        for group in section.field_groups:
            names: list[str] = []
            for key in group.keys:
                page = page_slug
                if is_visibility_key(key):
                    names.append(block_field_name(page, key, 'visible'))
                elif BLOCK_CONTENT_TYPES.get((page, key)) == 'image':
                    names.append(block_field_name(page, key, 'image'))
                else:
                    names.append(block_field_name(page, key, 'text_html'))
            grouped_fields.append((group.title, names))
    else:
        names = []
        for page, key in section.blocks:
            if is_visibility_key(key):
                names.append(block_field_name(page, key, 'visible'))
            elif BLOCK_CONTENT_TYPES.get((page, key)) == 'image':
                names.append(block_field_name(page, key, 'image'))
            else:
                names.append(block_field_name(page, key, 'text_html'))
        grouped_fields.append(('Контент', names))

    return [
        (
            group_title,
            [form[field_name] for field_name in field_names if field_name in form.fields],
        )
        for group_title, field_names in grouped_fields
    ]


def _image_previews(blocks) -> dict[str, str]:
    previews: dict[str, str] = {}
    for (page, key), block in blocks.items():
        if block.content_type == SiteBlock.ContentType.IMAGE and block.image:
            previews[block_field_name(page, key, 'image')] = block.image.url
    return previews
