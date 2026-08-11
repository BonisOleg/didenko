from urllib.parse import urlparse

from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

from src.pages.block_render import (
    get_block_image_url,
    get_block_text,
    is_section_visible,
)

register = template.Library()


def _normalize_nav_path(url):
    """Path без query/hash; root і trailing-slash нормалізовані."""
    if not url:
        return '/'
    path = urlparse(str(url)).path or '/'
    if not path.startswith('/'):
        path = f'/{path}'
    # «домашні» варіанти: '', '/', '/index', '/index.html'
    root_aliases = {'', '/', '/index', '/index/', '/index.html', '/index.html/'}
    if path.rstrip('/') in {'', '/index', '/index.html'} or path in root_aliases:
        return '/'
    if not path.endswith('/'):
        path = f'{path}/'
    return path


def is_nav_path_active(current_path, href):
    current = _normalize_nav_path(current_path)
    target = _normalize_nav_path(href)
    if target == '/':
        return current == '/'
    return current == target or current.startswith(target)


@register.simple_tag(takes_context=True)
def nav_aria_current(context, href):
    request = context.get('request')
    if not request or not is_nav_path_active(request.path, href):
        return ''
    return mark_safe(' aria-current="page"')


@register.simple_tag(takes_context=True)
def block_plain(context, page, key, fallback=''):
    site_blocks = context.get('site_blocks')
    return get_block_text(page, key, site_blocks=site_blocks, fallback=fallback)


@register.simple_tag(takes_context=True)
def section_visible(context, page, key):
    site_blocks = context.get('site_blocks')
    return is_section_visible(page, key, site_blocks=site_blocks)


@register.simple_tag(takes_context=True)
def block_image_url(context, page, key, fallback_static=''):
    site_blocks = context.get('site_blocks')
    return get_block_image_url(
        page,
        key,
        site_blocks=site_blocks,
        fallback_static=fallback_static,
    )


@register.simple_tag(takes_context=True)
def block_lines(context, page, key, fallback='', line_tag='br'):
    """Рядки з \\n → HTML з <br> (watermark)."""
    site_blocks = context.get('site_blocks')
    text = get_block_text(page, key, site_blocks=site_blocks, fallback=fallback)
    parts = [escape(line.strip()) for line in text.splitlines() if line.strip()]
    if not parts:
        return ''
    return mark_safe('<br>'.join(parts))
