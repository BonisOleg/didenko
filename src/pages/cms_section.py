"""Типи CMS-секцій."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class FieldGroup:
    title: str
    keys: tuple[str, ...]


@dataclass(frozen=True)
class ContentSection:
    slug: str
    page_slug: str
    title: str
    blocks: tuple[tuple[str, str], ...]
    sidebar_title: str = ''
    sidebar_icon: str = 'edit_note'
    preview_url: str = '/'
    description: str = ''
    visibility_key: str = ''
    field_groups: tuple[FieldGroup, ...] = field(default_factory=tuple)
    admin_model_name: str = ''
