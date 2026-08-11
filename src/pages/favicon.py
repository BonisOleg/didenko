"""URL фавіконок для публічного сайту та Unfold admin."""

from __future__ import annotations

from django.contrib.staticfiles.storage import staticfiles_storage

from src.pages.models import SiteSettings

DEFAULT_FAVICON_ICO = 'img/brand/favicon.ico'
DEFAULT_FAVICON_32 = 'img/brand/favicon-32.png'
DEFAULT_APPLE_TOUCH = 'img/brand/apple-touch-icon.png'


def _static_url(path: str) -> str:
    return staticfiles_storage.url(path)


def get_favicon_urls(site_settings: SiteSettings | None = None) -> dict[str, str]:
    """Повертає URL іконки / apple-touch з upload або static fallback."""
    if site_settings is None:
        try:
            site_settings = SiteSettings.load()
        except Exception:
            site_settings = None

    if site_settings and site_settings.favicon:
        url = site_settings.favicon.url
        return {
            'icon': url,
            'icon_32': url,
            'apple_touch': url,
            'is_custom': True,
        }

    return {
        'icon': _static_url(DEFAULT_FAVICON_ICO),
        'icon_32': _static_url(DEFAULT_FAVICON_32),
        'apple_touch': _static_url(DEFAULT_APPLE_TOUCH),
        'is_custom': False,
    }


def unfold_site_favicons(request=None) -> list[dict]:
    """Список фавіконок для UNFOLD['SITE_FAVICONS']."""
    urls = get_favicon_urls()
    if urls['is_custom']:
        return [
            {
                'href': urls['icon'],
                'rel': 'icon',
                'type': 'image/png',
                'sizes': 'any',
            },
            {
                'href': urls['apple_touch'],
                'rel': 'apple-touch-icon',
            },
        ]
    return [
        {
            'href': urls['icon'],
            'rel': 'icon',
            'type': 'image/x-icon',
            'sizes': 'any',
        },
        {
            'href': urls['icon_32'],
            'rel': 'icon',
            'type': 'image/png',
            'sizes': '32x32',
        },
        {
            'href': urls['apple_touch'],
            'rel': 'apple-touch-icon',
            'sizes': '180x180',
        },
    ]
