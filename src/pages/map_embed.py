"""Нормалізація Google Maps embed з URL або скопійованого <iframe>."""

from __future__ import annotations

from html.parser import HTMLParser
from urllib.parse import urlparse

from django.core.exceptions import ValidationError

ALLOWED_MAP_HOSTS = frozenset({
    'www.google.com',
    'maps.google.com',
    'google.com',
    'maps.google.com.ua',
    'www.google.com.ua',
})

MAP_EMBED_HELP_TEXT = (
    'Вставте код iframe з Google Maps (Поділитися → Вбудувати карту) '
    'або прямий embed URL. Зберігається лише безпечний src.'
)


class _IframeSrcParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.src = ''

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != 'iframe' or self.src:
            return
        for name, value in attrs:
            if name.lower() == 'src' and value:
                self.src = value.strip()
                return


def extract_iframe_src(raw: str) -> str:
    """Повертає src з першого <iframe>, або порожній рядок."""
    parser = _IframeSrcParser()
    try:
        parser.feed(raw)
        parser.close()
    except Exception:
        return ''
    return parser.src


def is_allowed_google_maps_embed(url: str) -> bool:
    try:
        parsed = urlparse(url)
    except ValueError:
        return False
    if parsed.scheme not in {'http', 'https'}:
        return False
    host = (parsed.hostname or '').lower()
    if host not in ALLOWED_MAP_HOSTS:
        return False
    path = parsed.path or ''
    return '/maps/embed' in path or path.startswith('/maps')


def normalize_google_maps_embed(raw: str) -> str:
    """
    Приймає iframe HTML або URL; повертає валідний embed URL.
    Порожній рядок — дозволено (карта прихована).
    """
    value = (raw or '').strip()
    if not value:
        return ''

    candidate = value
    if '<iframe' in value.lower():
        candidate = extract_iframe_src(value)
        if not candidate:
            raise ValidationError(
                'Не вдалося знайти src у коді iframe. '
                'Скопіюйте повний блок <iframe>…</iframe> з Google Maps.',
            )

    candidate = candidate.strip().strip('"').strip("'")
    if not is_allowed_google_maps_embed(candidate):
        raise ValidationError(
            'Дозволені лише embed-посилання Google Maps '
            '(www.google.com/maps/embed…).',
        )
    if len(candidate) > 2048:
        raise ValidationError('URL карти занадто довгий (макс. 2048 символів).')
    return candidate
