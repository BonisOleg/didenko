"""CMS-секції UI-хрому (шапка, футер, форми, логотипи)."""

from django.urls import reverse_lazy

from src.pages.cms_section import ContentSection, FieldGroup

SITE_UI_SECTIONS: tuple[ContentSection, ...] = (
    ContentSection(
        slug='brand',
        page_slug='site',
        title='Бренд і логотипи',
        sidebar_title='Бренд / логотипи',
        sidebar_icon='branding_watermark',
        preview_url='/',
        description='Назва, підпис і логотипи шапки/футера.',
        admin_model_name='sitebrandsettings',
        blocks=(
            ('site', 'brand_name'),
            ('site', 'brand_title'),
            ('site', 'logo_header'),
            ('site', 'logo_footer'),
        ),
        field_groups=(
            FieldGroup('Текст', ('brand_name', 'brand_title')),
            FieldGroup('Логотипи', ('logo_header', 'logo_footer')),
        ),
    ),
    ContentSection(
        slug='navigation',
        page_slug='site',
        title='Навігація',
        sidebar_title='Навігація',
        sidebar_icon='menu',
        preview_url='/',
        description='Пункти меню, CTA та видимість елементів шапки.',
        admin_model_name='sitenavigationsettings',
        blocks=(
            ('site', 'nav_toggle_label'),
            ('site', 'nav_open_aria'),
            ('site', 'nav_aria'),
            ('site', 'nav_home_visible'),
            ('site', 'nav_home_label'),
            ('site', 'nav_home_href'),
            ('site', 'nav_about_visible'),
            ('site', 'nav_about_label'),
            ('site', 'nav_about_href'),
            ('site', 'nav_services_visible'),
            ('site', 'nav_services_label'),
            ('site', 'nav_services_href'),
            ('site', 'nav_blog_visible'),
            ('site', 'nav_blog_label'),
            ('site', 'nav_blog_href'),
            ('site', 'nav_contacts_visible'),
            ('site', 'nav_contacts_label'),
            ('site', 'nav_contacts_href'),
            ('site', 'nav_phone_visible'),
            ('site', 'nav_cta_visible'),
            ('site', 'nav_cta_label'),
            ('site', 'nav_cta_href'),
        ),
        field_groups=(
            FieldGroup('Доступність', ('nav_toggle_label', 'nav_open_aria', 'nav_aria')),
            FieldGroup(
                'Головна',
                ('nav_home_visible', 'nav_home_label', 'nav_home_href'),
            ),
            FieldGroup(
                'Про мене',
                ('nav_about_visible', 'nav_about_label', 'nav_about_href'),
            ),
            FieldGroup(
                'Послуги',
                ('nav_services_visible', 'nav_services_label', 'nav_services_href'),
            ),
            FieldGroup(
                'Блог',
                ('nav_blog_visible', 'nav_blog_label', 'nav_blog_href'),
            ),
            FieldGroup(
                'Контакти',
                ('nav_contacts_visible', 'nav_contacts_label', 'nav_contacts_href'),
            ),
            FieldGroup(
                'Дії',
                ('nav_phone_visible', 'nav_cta_visible', 'nav_cta_label', 'nav_cta_href'),
            ),
        ),
    ),
    ContentSection(
        slug='footer',
        page_slug='site',
        title='Footer',
        sidebar_title='Footer',
        sidebar_icon='web_asset',
        preview_url='/',
        description='Тексти підвалу сайту.',
        admin_model_name='sitefootersettings',
        blocks=(
            ('site', 'footer_tagline'),
            ('site', 'footer_nav_heading'),
            ('site', 'footer_contacts_heading'),
            ('site', 'footer_messengers_heading'),
            ('site', 'footer_hours_prefix'),
            ('site', 'footer_policy_label'),
            ('site', 'footer_policy_href'),
            ('site', 'footer_madeby_label'),
            ('site', 'footer_madeby_url'),
            ('site', 'footer_nav_aria'),
        ),
        field_groups=(
            FieldGroup('Бренд', ('footer_tagline',)),
            FieldGroup(
                'Заголовки',
                (
                    'footer_nav_heading',
                    'footer_contacts_heading',
                    'footer_messengers_heading',
                    'footer_hours_prefix',
                ),
            ),
            FieldGroup(
                'Посилання',
                (
                    'footer_policy_label',
                    'footer_policy_href',
                    'footer_madeby_label',
                    'footer_madeby_url',
                    'footer_nav_aria',
                ),
            ),
        ),
    ),
    ContentSection(
        slug='forms',
        page_slug='site',
        title='Форми та модалки',
        sidebar_title='Форми / модалки',
        sidebar_icon='edit_note',
        preview_url='/#lead-form',
        description='Лейбли форм, success-тексти, модальне вікно заявки.',
        admin_model_name='siteformssettings',
        blocks=(
            ('site', 'form_label_name'),
            ('site', 'form_label_phone'),
            ('site', 'form_label_email'),
            ('site', 'form_consent_prefix'),
            ('site', 'form_consent_link'),
            ('site', 'form_submit'),
            ('site', 'form_success_title'),
            ('site', 'form_success_text'),
            ('site', 'lead_modal_eyebrow'),
            ('site', 'lead_modal_title'),
            ('site', 'lead_modal_lead'),
            ('site', 'modal_close_aria'),
            ('site', 'service_modal_loading'),
        ),
        field_groups=(
            FieldGroup(
                'Поля форми',
                (
                    'form_label_name',
                    'form_label_phone',
                    'form_label_email',
                    'form_consent_prefix',
                    'form_consent_link',
                    'form_submit',
                ),
            ),
            FieldGroup('Успіх', ('form_success_title', 'form_success_text')),
            FieldGroup(
                'Модалки',
                (
                    'lead_modal_eyebrow',
                    'lead_modal_title',
                    'lead_modal_lead',
                    'modal_close_aria',
                    'service_modal_loading',
                ),
            ),
        ),
    ),
)


def build_ui_sidebar_items() -> list[dict]:
    return [
        {
            'title': section.sidebar_title or section.title,
            'icon': section.sidebar_icon,
            'link': reverse_lazy(f'admin:pages_{section.admin_model_name}_changelist'),
        }
        for section in SITE_UI_SECTIONS
    ]
