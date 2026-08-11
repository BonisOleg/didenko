"""Реєстр CMS-секцій (контент сторінок)."""

from django.urls import reverse_lazy

from src.pages.block_defaults import BLOCK_FIELD_LABELS
from src.pages.cms_section import ContentSection, FieldGroup
from src.pages.site_ui_registry import SITE_UI_SECTIONS

CONTENT_SECTIONS: tuple[ContentSection, ...] = (
    ContentSection(
        slug='hero',
        page_slug='home',
        title='Головна — Hero',
        sidebar_title='Головна · Hero',
        sidebar_icon='image',
        preview_url='/',
        description='Перший екран: бренд, заголовок, фото, кнопки.',
        visibility_key='hero_section_visible',
        admin_model_name='homeherosettings',
        blocks=(
            ('home', 'hero_brand'),
            ('home', 'hero_title'),
            ('home', 'hero_sub'),
            ('home', 'hero_image'),
            ('home', 'hero_shade_visible'),
            ('home', 'hero_cta_label'),
            ('home', 'hero_cta_href'),
            ('home', 'hero_secondary_label'),
            ('home', 'hero_secondary_href'),
        ),
        field_groups=(
            FieldGroup('Текст', ('hero_brand', 'hero_title', 'hero_sub')),
            FieldGroup('Фото', ('hero_image', 'hero_shade_visible')),
            FieldGroup(
                'Кнопки',
                (
                    'hero_cta_label',
                    'hero_cta_href',
                    'hero_secondary_label',
                    'hero_secondary_href',
                ),
            ),
        ),
    ),
    ContentSection(
        slug='audience',
        page_slug='home',
        title='Головна — Для кого',
        sidebar_title='Головна · Для кого',
        sidebar_icon='group',
        preview_url='/#audience',
        description='Заголовки секції. Пункти списку — у «Блоки головної».',
        visibility_key='audience_section_visible',
        admin_model_name='homeaudiencesettings',
        blocks=(
            ('home', 'audience_eyebrow'),
            ('home', 'audience_title'),
            ('home', 'audience_intro'),
            ('home', 'audience_cta_text'),
            ('home', 'audience_cta_label'),
            ('home', 'audience_cta_href'),
        ),
        field_groups=(
            FieldGroup(
                'Секція',
                ('audience_eyebrow', 'audience_title', 'audience_intro'),
            ),
            FieldGroup(
                'CTA',
                ('audience_cta_text', 'audience_cta_label', 'audience_cta_href'),
            ),
        ),
    ),
    ContentSection(
        slug='services',
        page_slug='home',
        title='Головна — Послуги',
        sidebar_title='Головна · Послуги',
        sidebar_icon='gavel',
        preview_url='/#services',
        description='Заголовки превʼю послуг. Картки — з каталогу «Послуги».',
        visibility_key='services_section_visible',
        admin_model_name='homeservicessettings',
        blocks=(
            ('home', 'services_eyebrow'),
            ('home', 'services_title'),
            ('home', 'services_intro'),
            ('home', 'services_card_more'),
            ('home', 'services_footer_cta'),
            ('home', 'services_footer_href'),
        ),
        field_groups=(
            FieldGroup(
                'Секція',
                ('services_eyebrow', 'services_title', 'services_intro'),
            ),
            FieldGroup(
                'Кнопки',
                ('services_card_more', 'services_footer_cta', 'services_footer_href'),
            ),
        ),
    ),
    ContentSection(
        slug='advantages',
        page_slug='home',
        title='Головна — Переваги',
        sidebar_title='Головна · Переваги',
        sidebar_icon='verified',
        preview_url='/#advantages',
        description='Заголовки та фото. Пункти — у «Блоки головної» (advantages).',
        visibility_key='advantages_section_visible',
        admin_model_name='homeadvantagessettings',
        blocks=(
            ('home', 'advantages_eyebrow'),
            ('home', 'advantages_title'),
            ('home', 'advantages_intro'),
            ('home', 'advantages_image'),
        ),
        field_groups=(
            FieldGroup(
                'Секція',
                ('advantages_eyebrow', 'advantages_title', 'advantages_intro'),
            ),
            FieldGroup('Фото', ('advantages_image',)),
        ),
    ),
    ContentSection(
        slug='blog',
        page_slug='home',
        title='Головна — Блог',
        sidebar_title='Головна · Блог',
        sidebar_icon='newspaper',
        preview_url='/#blog',
        description='Заголовки превʼю блогу на головній.',
        visibility_key='blog_section_visible',
        admin_model_name='homeblogsettings',
        blocks=(
            ('home', 'blog_eyebrow'),
            ('home', 'blog_title'),
            ('home', 'blog_intro'),
            ('home', 'blog_filter_all'),
            ('home', 'blog_filter_cases'),
            ('home', 'blog_filter_news'),
            ('home', 'blog_footer_cta'),
        ),
        field_groups=(
            FieldGroup('Секція', ('blog_eyebrow', 'blog_title', 'blog_intro')),
            FieldGroup(
                'Фільтри / CTA',
                (
                    'blog_filter_all',
                    'blog_filter_cases',
                    'blog_filter_news',
                    'blog_footer_cta',
                ),
            ),
        ),
    ),
    ContentSection(
        slug='lead',
        page_slug='home',
        title='Головна — Форма заявки',
        sidebar_title='Головна · Заявка',
        sidebar_icon='mail',
        preview_url='/#lead-form',
        description='Тексти CTA-панелі з формою на головній.',
        visibility_key='lead_section_visible',
        admin_model_name='homeleadsettings',
        blocks=(
            ('home', 'lead_eyebrow'),
            ('home', 'lead_title'),
            ('home', 'lead_intro'),
        ),
        field_groups=(
            FieldGroup('Секція', ('lead_eyebrow', 'lead_title', 'lead_intro')),
        ),
    ),
    ContentSection(
        slug='page',
        page_slug='services',
        title='Послуги — сторінка',
        sidebar_title='Послуги · Сторінка',
        sidebar_icon='work',
        preview_url='/posluhy/',
        description='Hero, каталог, процес, CTA. Кроки процесу — окрема модель.',
        visibility_key='page_section_visible',
        admin_model_name='servicespagesettings',
        blocks=(
            ('services', 'hero_badge'),
            ('services', 'hero_sub'),
            ('services', 'catalog_section_visible'),
            ('services', 'catalog_eyebrow'),
            ('services', 'catalog_intro'),
            ('services', 'catalog_card_more'),
            ('services', 'catalog_empty'),
            ('services', 'process_section_visible'),
            ('services', 'process_eyebrow'),
            ('services', 'process_title'),
            ('services', 'process_intro'),
            ('services', 'cta_section_visible'),
            ('services', 'cta_eyebrow'),
            ('services', 'cta_title'),
            ('services', 'cta_intro'),
            ('services', 'cta_form_title'),
            ('services', 'detail_badge'),
            ('services', 'detail_deliverables_title'),
            ('services', 'detail_result_title'),
            ('services', 'detail_timeline_label'),
            ('services', 'modal_eyebrow'),
            ('services', 'modal_deliverables_title'),
            ('services', 'modal_result_title'),
            ('services', 'modal_timeline_label'),
            ('services', 'modal_cta'),
            ('services', 'modal_full_page'),
        ),
        field_groups=(
            FieldGroup('Hero', ('hero_badge', 'hero_sub')),
            FieldGroup(
                'Каталог',
                (
                    'catalog_section_visible',
                    'catalog_eyebrow',
                    'catalog_intro',
                    'catalog_card_more',
                    'catalog_empty',
                ),
            ),
            FieldGroup(
                'Процес',
                (
                    'process_section_visible',
                    'process_eyebrow',
                    'process_title',
                    'process_intro',
                ),
            ),
            FieldGroup(
                'CTA',
                (
                    'cta_section_visible',
                    'cta_eyebrow',
                    'cta_title',
                    'cta_intro',
                    'cta_form_title',
                ),
            ),
            FieldGroup(
                'Деталь / модалка',
                (
                    'detail_badge',
                    'detail_deliverables_title',
                    'detail_result_title',
                    'detail_timeline_label',
                    'modal_eyebrow',
                    'modal_deliverables_title',
                    'modal_result_title',
                    'modal_timeline_label',
                    'modal_cta',
                    'modal_full_page',
                ),
            ),
        ),
    ),
    ContentSection(
        slug='page',
        page_slug='contacts',
        title='Контакти — сторінка',
        sidebar_title='Контакти · Сторінка',
        sidebar_icon='contact_page',
        preview_url='/kontakty/',
        description='Тексти сторінки контактів. Телефон/email — у Налаштуваннях.',
        visibility_key='page_section_visible',
        admin_model_name='contactspagesettings',
        blocks=(
            ('contacts', 'hero_badge'),
            ('contacts', 'hero_sub'),
            ('contacts', 'info_badge'),
            ('contacts', 'info_title'),
            ('contacts', 'label_phone'),
            ('contacts', 'label_email'),
            ('contacts', 'label_region'),
            ('contacts', 'email_copy_hint'),
            ('contacts', 'email_copied'),
            ('contacts', 'region_suffix'),
            ('contacts', 'form_title'),
            ('contacts', 'form_subtext'),
        ),
        field_groups=(
            FieldGroup('Hero', ('hero_badge', 'hero_sub')),
            FieldGroup(
                'Колонка контактів',
                (
                    'info_badge',
                    'info_title',
                    'label_phone',
                    'label_email',
                    'label_region',
                    'email_copy_hint',
                    'email_copied',
                    'region_suffix',
                ),
            ),
            FieldGroup('Форма', ('form_title', 'form_subtext')),
        ),
    ),
    ContentSection(
        slug='page',
        page_slug='blog',
        title='Блог — сторінка',
        sidebar_title='Блог · Сторінка',
        sidebar_icon='article',
        preview_url='/blog/',
        description='Chrome блогу: badge, порожні стани, печатка карток.',
        visibility_key='page_section_visible',
        admin_model_name='blogpagesettings',
        blocks=(
            ('blog', 'hero_badge'),
            ('blog', 'hero_sub'),
            ('blog', 'load_more'),
            ('blog', 'empty'),
            ('blog', 'share_title'),
            ('blog', 'seal_text'),
            ('blog', 'seal_sub'),
            ('blog', 'watermark'),
        ),
        field_groups=(
            FieldGroup('Hero', ('hero_badge', 'hero_sub')),
            FieldGroup('Списки', ('load_more', 'empty', 'share_title')),
            FieldGroup('Картка', ('seal_text', 'seal_sub', 'watermark')),
        ),
    ),
)

ALL_CONTENT_SECTIONS: tuple[ContentSection, ...] = CONTENT_SECTIONS + SITE_UI_SECTIONS


def get_section(page_slug: str, section_slug: str) -> ContentSection | None:
    for section in ALL_CONTENT_SECTIONS:
        if section.page_slug == page_slug and section.slug == section_slug:
            return section
    return None


def iter_section_blocks(section: ContentSection) -> tuple[tuple[str, str], ...]:
    keys: list[tuple[str, str]] = list(section.blocks)
    if section.visibility_key:
        keys.insert(0, (section.page_slug, section.visibility_key))
    return tuple(keys)


def all_registry_block_keys() -> tuple[tuple[str, str], ...]:
    seen: set[tuple[str, str]] = set()
    ordered: list[tuple[str, str]] = []
    for section in ALL_CONTENT_SECTIONS:
        for key in iter_section_blocks(section):
            if key not in seen:
                seen.add(key)
                ordered.append(key)
    return tuple(ordered)


def build_content_sidebar_items() -> list[dict]:
    return [
        {
            'title': section.sidebar_title or section.title,
            'icon': section.sidebar_icon,
            'link': reverse_lazy(f'admin:pages_{section.admin_model_name}_changelist'),
        }
        for section in CONTENT_SECTIONS
    ]


def build_ui_sidebar_items() -> list[dict]:
    from src.pages.site_ui_registry import build_ui_sidebar_items as _build

    return _build()


def label_for_block(page: str, key: str) -> str:
    return BLOCK_FIELD_LABELS.get((page, key), key.replace('_', ' ').capitalize())
