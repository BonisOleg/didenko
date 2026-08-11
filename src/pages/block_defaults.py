"""Константи CMS-блоків без імпорту моделей Django."""

from typing import Literal

BlockKey = tuple[str, str]
ContentTypeName = Literal['text', 'image', 'url']

BLOCK_DEFAULTS: dict[BlockKey, str] = {
    # --- Home hero ---
    ('home', 'hero_section_visible'): '1',
    ('home', 'hero_brand'): 'Арбітражна керуюча Діденко В. В.',
    (
        'home',
        'hero_title',
    ): 'Законне списання боргів та банкрутство фізичних осіб «під ключ»',
    (
        'home',
        'hero_sub',
    ): (
        'Законне списання боргів відповідно до Кодексу України '
        'з процедур банкрутства.'
    ),
    ('home', 'hero_shade_visible'): '1',
    ('home', 'hero_cta_label'): 'Залишити заявку',
    ('home', 'hero_cta_href'): '#lead-form',
    ('home', 'hero_secondary_label'): 'Для кого це',
    ('home', 'hero_secondary_href'): '#audience',
    # --- Home audience ---
    ('home', 'audience_section_visible'): '1',
    ('home', 'audience_eyebrow'): 'Аудиторія',
    ('home', 'audience_title'): 'Вам потрібна допомога, якщо ви:',
    (
        'home',
        'audience_intro',
    ): 'Сигнали, коли варто звернутися за супроводом процедури неплатоспроможності.',
    (
        'home',
        'audience_cta_text',
    ): 'Безкоштовно оцініть свої шанси на списання боргів.',
    ('home', 'audience_cta_label'): 'Оцінити шанси',
    ('home', 'audience_cta_href'): '#lead-form',
    # --- Home services ---
    ('home', 'services_section_visible'): '1',
    ('home', 'services_eyebrow'): 'Послуги',
    ('home', 'services_title'): 'Мої послуги',
    (
        'home',
        'services_intro',
    ): (
        'Повний супровід процедури неплатоспроможності — від оцінки ризиків '
        'до рішення суду про списання боргів.'
    ),
    ('home', 'services_card_more'): 'Детальніше',
    ('home', 'services_footer_cta'): 'Отримати розрахунок вартості',
    ('home', 'services_footer_href'): '#lead-form',
    # --- Home advantages ---
    ('home', 'advantages_section_visible'): '1',
    ('home', 'advantages_eyebrow'): 'Довіра',
    ('home', 'advantages_title'): 'Чому обирають мене',
    (
        'home',
        'advantages_intro',
    ): (
        'Структурований супровід, прозорі умови та персональна відповідальність '
        'на кожному етапі процедури.'
    ),
    # --- Home blog ---
    ('home', 'blog_section_visible'): '1',
    ('home', 'blog_eyebrow'): 'Блог і кейси',
    ('home', 'blog_title'): 'Останні матеріали',
    (
        'home',
        'blog_intro',
    ): 'Практика, аналітика та реальні приклади успішного списання боргів.',
    ('home', 'blog_filter_all'): 'Усі матеріали',
    ('home', 'blog_filter_cases'): 'Реальні кейси',
    ('home', 'blog_filter_news'): 'Аналітика та новини',
    ('home', 'blog_footer_cta'): 'Усі матеріали та кейси',
    # --- Home lead ---
    ('home', 'lead_section_visible'): '1',
    ('home', 'lead_eyebrow'): 'Звʼязок',
    ('home', 'lead_title'): 'Залишити заявку',
    (
        'home',
        'lead_intro',
    ): (
        'Залиште контакти — проведу первинну перевірку ситуації та підкажу наступні кроки. '
        'Без зобовʼязань і без прихованих платежів.'
    ),
    # --- Site header / brand ---
    ('site', 'brand_name'): 'Діденко В. В.',
    ('site', 'brand_title'): 'Арбітражна керуюча',
    ('site', 'nav_toggle_label'): 'Меню',
    ('site', 'nav_open_aria'): 'Відкрити меню',
    ('site', 'nav_aria'): 'Головна навігація',
    ('site', 'nav_home_label'): 'Головна',
    ('site', 'nav_home_href'): '/',
    ('site', 'nav_about_label'): 'Про мене',
    ('site', 'nav_about_href'): '/pro-nas/',
    ('site', 'nav_services_label'): 'Послуги',
    ('site', 'nav_services_href'): '/posluhy/',
    ('site', 'nav_blog_label'): 'Блог',
    ('site', 'nav_blog_href'): '/blog/',
    ('site', 'nav_contacts_label'): 'Контакти',
    ('site', 'nav_contacts_href'): '/kontakty/',
    ('site', 'nav_cta_label'): 'Залишити заявку',
    ('site', 'nav_cta_href'): '/#lead-form',
    ('site', 'nav_home_visible'): '1',
    ('site', 'nav_about_visible'): '1',
    ('site', 'nav_services_visible'): '1',
    ('site', 'nav_blog_visible'): '1',
    ('site', 'nav_contacts_visible'): '1',
    ('site', 'nav_cta_visible'): '1',
    ('site', 'nav_phone_visible'): '1',
    # --- Site footer ---
    (
        'site',
        'footer_tagline',
    ): 'Законне списання боргів і банкрутство фізичних осіб під ключ',
    ('site', 'footer_nav_heading'): 'Навігація',
    ('site', 'footer_contacts_heading'): 'Контакти',
    ('site', 'footer_messengers_heading'): 'Месенджери',
    ('site', 'footer_hours_prefix'): 'Графік роботи:',
    ('site', 'footer_policy_label'): 'Політика конфіденційності',
    ('site', 'footer_policy_href'): '/polityka-konfidentsiynosti/',
    ('site', 'footer_madeby_label'): 'Сайт від PrometeyLabs',
    ('site', 'footer_madeby_url'): 'https://prometeylabs.com',
    ('site', 'footer_nav_aria'): 'Навігація в підвалі',
    # --- Forms / UI chrome ---
    ('site', 'form_label_name'): 'Імʼя',
    ('site', 'form_label_phone'): 'Телефон',
    ('site', 'form_label_email'): 'Email',
    ('site', 'form_consent_prefix'): 'Погоджуюсь з',
    ('site', 'form_consent_link'): 'політикою конфіденційності',
    ('site', 'form_submit'): 'Надіслати заявку',
    ('site', 'form_success_title'): 'Дякуємо! Вашу заявку прийнято',
    (
        'site',
        'form_success_text',
    ): 'Звʼяжусь з вами найближчим часом для первинної перевірки ситуації.',
    ('site', 'lead_modal_eyebrow'): 'Консультація',
    ('site', 'lead_modal_title'): 'Залишити заявку',
    (
        'site',
        'lead_modal_lead',
    ): (
        'Оціню вашу ситуацію та запропоную оптимальний правовий шлях '
        'у межах законодавства України.'
    ),
    ('site', 'modal_close_aria'): 'Закрити',
    ('site', 'service_modal_loading'): 'Завантаження…',
    # --- Services page ---
    ('services', 'page_section_visible'): '1',
    ('services', 'hero_badge'): 'ПОСЛУГИ ТА СУПРОВІД',
    (
        'services',
        'hero_sub',
    ): (
        'Професійна допомога на кожному етапі процедури неплатоспроможності '
        'фізичних осіб відповідно до Кодексу України з процедур банкрутства.'
    ),
    ('services', 'catalog_section_visible'): '1',
    ('services', 'catalog_eyebrow'): 'Каталог',
    (
        'services',
        'catalog_intro',
    ): (
        'Комплексна правова допомога: від аналізу фінансового стану '
        'до остаточного списання боргів у судовому порядку.'
    ),
    ('services', 'catalog_card_more'): 'Докладніше про послугу',
    ('services', 'catalog_empty'): 'Послуги зʼявляться найближчим часом.',
    ('services', 'process_section_visible'): '1',
    ('services', 'process_eyebrow'): 'Процес',
    ('services', 'process_title'): 'Як проходить співпраця',
    (
        'services',
        'process_intro',
    ): 'Прозорий маршрут від першої розмови до рішення суду.',
    ('services', 'cta_section_visible'): '1',
    ('services', 'cta_eyebrow'): 'Консультація',
    ('services', 'cta_title'): 'Потрібна допомога у виборі необхідної послуги?',
    (
        'services',
        'cta_intro',
    ): (
        'Залиште контактні дані для первинного аналізу вашої справи '
        'арбітражною керуючою.'
    ),
    ('services', 'cta_form_title'): 'Отримати безкоштовну консультацію',
    ('services', 'detail_badge'): 'ПОСЛУГА',
    ('services', 'detail_deliverables_title'): 'Що входить у послугу',
    ('services', 'detail_result_title'): 'Очікуваний результат',
    ('services', 'detail_timeline_label'): 'Терміни:',
    ('services', 'modal_eyebrow'): 'Послуга',
    ('services', 'modal_deliverables_title'): 'Що входить у послугу',
    ('services', 'modal_result_title'): 'Очікуваний результат',
    ('services', 'modal_timeline_label'): 'Терміни виконання',
    ('services', 'modal_cta'): 'Замовити послугу',
    ('services', 'modal_full_page'): 'Повна сторінка послуги',
    # --- Contacts page ---
    ('contacts', 'page_section_visible'): '1',
    ('contacts', 'hero_badge'): 'ЗВʼЯЗОК',
    (
        'contacts',
        'hero_sub',
    ): (
        'Звʼяжіться для первинної консультації щодо процедури банкрутства '
        'та списання боргів.'
    ),
    ('contacts', 'info_badge'): 'КОНТАКТИ',
    ('contacts', 'info_title'): 'Звʼяжіться зі мною',
    ('contacts', 'label_phone'): 'Телефон',
    ('contacts', 'label_email'): 'Email',
    ('contacts', 'label_region'): 'Регіон роботи',
    ('contacts', 'email_copy_hint'): 'Натисніть, щоб скопіювати',
    ('contacts', 'email_copied'): 'Скопійовано',
    ('contacts', 'region_suffix'): '(Консультації та супровід)',
    ('contacts', 'form_title'): 'Залишити заявку',
    (
        'contacts',
        'form_subtext',
    ): 'Заповніть форму, і я звʼяжуся з вами для аналізу вашої ситуації.',
    # --- Blog page ---
    ('blog', 'page_section_visible'): '1',
    ('blog', 'hero_badge'): 'Практика та аналітика',
    (
        'blog',
        'hero_sub',
    ): (
        'Актуальна судова практика, розʼяснення Кодексу України з процедур банкрутства '
        'та реальні історії списання боргів.'
    ),
    ('blog', 'load_more'): 'Завантажити ще матеріали',
    ('blog', 'empty'): 'Записів у цій категорії поки немає.',
    ('blog', 'share_title'): 'Поділитися',
    ('blog', 'seal_text'): 'АК',
    ('blog', 'seal_sub'): 'Діденко',
    (
        'blog',
        'watermark',
    ): 'Кодекс України\nз процедур банкрутства',
}


from src.pages.block_field_meta import (  # noqa: F401
    BLOCK_CONTENT_TYPES,
    BLOCK_FIELD_HELP,
    BLOCK_FIELD_LABELS,
    INLINE_KEYS,
    MULTILINE_KEYS,
)


def is_visibility_key(key: str) -> bool:
    return key.endswith('_visible')


def default_for_key(page: str, key: str) -> str:
    return BLOCK_DEFAULTS.get((page, key), '')
