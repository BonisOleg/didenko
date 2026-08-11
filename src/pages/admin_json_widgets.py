"""Інтуїтивні віджети для JSON-списків в адмінці."""

from __future__ import annotations

import json
from typing import Any

from django import forms
from django.forms.utils import flatatt
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from unfold.widgets import INPUT_CLASSES, TEXTAREA_CLASSES

from src.pages.admin_site_content_widgets import cms_control_classes


_STRIP_WIDTH = frozenset({'max-w-2xl', 'max-w-4xl'})


def _input_class() -> str:
    return ' '.join(
        c for c in cms_control_classes(list(INPUT_CLASSES)) if c not in _STRIP_WIDTH
    )


def _textarea_class() -> str:
    return ' '.join(
        c for c in cms_control_classes(list(TEXTAREA_CLASSES)) if c not in _STRIP_WIDTH
    )


class _ProjectTemplateWidget(forms.Widget):
    """Рендер через project TEMPLATES (DIRS + apps), не лише django.forms."""

    def _render(self, template_name, context, renderer=None):
        return mark_safe(render_to_string(template_name, context))


class JsonStringListWidget(_ProjectTemplateWidget):
    """Динамічний список рядків з кнопками Додати / Видалити."""

    template_name = 'admin/widgets/json_string_list.html'

    class Media:
        css = {'all': ('css/admin/json_list_widget.css',)}
        js = ('js/admin/json_list_widget.js',)

    def __init__(self, attrs=None, *, item_label: str = 'Пункт', add_label: str = 'Додати пункт'):
        super().__init__(attrs)
        self.item_label = item_label
        self.add_label = add_label

    def format_value(self, value: Any) -> list[str]:
        if value is None or value == '':
            return ['']
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                return [value]
        if not isinstance(value, list):
            return ['']
        items = [str(v) for v in value if v is not None and str(v).strip()]
        return items or ['']

    def value_from_datadict(self, data, files, name) -> list[str]:
        return [v.strip() for v in data.getlist(name) if v is not None and str(v).strip()]

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        items = self.format_value(value)
        final_attrs = self.build_attrs(attrs)
        final_attrs.pop('id', None)
        final_attrs.pop('class', None)
        final_attrs.pop('rows', None)
        final_attrs['name'] = name
        context['widget'].update(
            {
                'items': items,
                'item_label': self.item_label,
                'add_label': self.add_label,
                'input_class': _textarea_class(),
                'item_attrs': flatatt(final_attrs),
            }
        )
        return context


class JsonObjectListWidget(_ProjectTemplateWidget):
    """Динамічний список обʼєктів (напр. title/text або label/url)."""

    template_name = 'admin/widgets/json_object_list.html'

    class Media:
        css = {'all': ('css/admin/json_list_widget.css',)}
        js = ('js/admin/json_list_widget.js',)

    def __init__(
        self,
        attrs=None,
        *,
        item_fields: list[tuple[str, str, str]] | None = None,
        add_label: str = 'Додати пункт',
    ):
        """
        item_fields: [(key, label, 'input'|'textarea'), ...]
        """
        super().__init__(attrs)
        self.item_fields = item_fields or [
            ('title', 'Заголовок', 'input'),
            ('text', 'Текст', 'textarea'),
        ]
        self.add_label = add_label

    def format_value(self, value: Any) -> list[dict[str, str]]:
        keys = [k for k, _, _ in self.item_fields]
        empty = {k: '' for k in keys}
        if value is None or value == '':
            return [empty.copy()]
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                return [empty.copy()]
        if not isinstance(value, list):
            return [empty.copy()]
        items: list[dict[str, str]] = []
        for raw in value:
            if isinstance(raw, dict):
                items.append({k: str(raw.get(k) or '') for k in keys})
            elif isinstance(raw, str) and raw.strip():
                first = keys[0]
                row = empty.copy()
                row[first] = raw.strip()
                items.append(row)
        return items or [empty.copy()]

    def value_from_datadict(self, data, files, name) -> list[dict[str, str]]:
        keys = [k for k, _, _ in self.item_fields]
        lists = {k: data.getlist(f'{name}__{k}') for k in keys}
        count = max((len(v) for v in lists.values()), default=0)
        items: list[dict[str, str]] = []
        for i in range(count):
            item = {
                k: (lists[k][i].strip() if i < len(lists[k]) else '')
                for k in keys
            }
            if any(item.values()):
                items.append(item)
        return items

    def _field_meta(self, name: str, item: dict[str, str] | None = None) -> list[dict]:
        meta = []
        for key, label, kind in self.item_fields:
            css = _textarea_class() if kind == 'textarea' else _input_class()
            meta.append(
                {
                    'key': key,
                    'label': label,
                    'kind': kind,
                    'css': css,
                    'name': f'{name}__{key}',
                    'value': (item or {}).get(key, ''),
                }
            )
        return meta

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        items = self.format_value(value)
        rows = [{'fields': self._field_meta(name, item)} for item in items]
        context['widget'].update(
            {
                'rows': rows,
                'empty_fields': self._field_meta(name),
                'add_label': self.add_label,
            }
        )
        return context


class JsonStringListField(forms.Field):
    widget = JsonStringListWidget

    def __init__(self, *, item_label: str = 'Пункт', add_label: str = 'Додати пункт', **kwargs):
        kwargs.setdefault('required', False)
        super().__init__(**kwargs)
        self.widget = JsonStringListWidget(item_label=item_label, add_label=add_label)

    def to_python(self, value):
        if not value:
            return []
        if isinstance(value, list):
            return [str(v).strip() for v in value if str(v).strip()]
        return []


class JsonObjectListField(forms.Field):
    widget = JsonObjectListWidget

    def __init__(
        self,
        *,
        item_fields: list[tuple[str, str, str]] | None = None,
        add_label: str = 'Додати пункт',
        **kwargs,
    ):
        kwargs.setdefault('required', False)
        super().__init__(**kwargs)
        self.widget = JsonObjectListWidget(item_fields=item_fields, add_label=add_label)

    def to_python(self, value):
        if not value:
            return []
        if isinstance(value, list):
            return value
        return []
