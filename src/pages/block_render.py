"""Хелпери читання SiteBlock для шаблонів і views."""


def get_block_text(page: str, key: str, site_blocks=None, fallback: str = '') -> str:
    if site_blocks is None:
        from src.pages.block_defaults import default_for_key

        return default_for_key(page, key) or fallback
    block = site_blocks.get(f'{page}.{key}')
    if block is None or not block.text_html:
        from src.pages.block_defaults import default_for_key

        return default_for_key(page, key) or fallback
    return block.text_html


def is_section_visible(page: str, visibility_key: str, site_blocks=None) -> bool:
    value = get_block_text(page, visibility_key, site_blocks=site_blocks, fallback='1')
    return value not in {'0', 'false', 'False', ''}


def get_block_image_url(
    page: str,
    key: str,
    site_blocks=None,
    fallback_static: str = '',
) -> str:
    from django.templatetags.static import static

    if site_blocks is not None:
        block = site_blocks.get(f'{page}.{key}')
        if block is not None and block.image:
            return block.image.url
    if fallback_static:
        return static(fallback_static)
    return ''


def get_block_url(page: str, key: str, site_blocks=None, fallback: str = '') -> str:
    if site_blocks is not None:
        block = site_blocks.get(f'{page}.{key}')
        if block is not None and block.link_url:
            return block.link_url
    return get_block_text(page, key, site_blocks=site_blocks, fallback=fallback)


def get_block_url_label(page: str, key: str, site_blocks=None, fallback: str = '') -> str:
    if site_blocks is not None:
        block = site_blocks.get(f'{page}.{key}')
        if block is not None and block.link_label:
            return block.link_label
    return fallback
