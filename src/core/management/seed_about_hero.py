"""Seed фото hero для сторінки «Про мене» з static (або локального media)."""

from __future__ import annotations

from pathlib import Path

from django.conf import settings
from django.core.files import File

from src.pages.models import Page

# У git/Docker — оптимізований 800×1000 WebP (≤1 МБ, 4:5).
# Локально fallback на оригінал у media/ (gitignored).
_PORTRAIT_CANDIDATES = (
    ('static', 'img', 'about', 'portrait.webp'),
    ('media', 'about', 'IMG_3048_ec6b1hm.JPG'),
    ('media', 'about', 'IMG_3048.JPG'),
)

_DEFAULT_ALT = 'Діденко Валерія Валеріївна'
_DEFAULT_CAPTION = 'Арбітражна керуюча • Практичний досвід'


def _candidate_paths() -> list[Path]:
    base = Path(settings.BASE_DIR)
    return [base.joinpath(*parts) for parts in _PORTRAIT_CANDIDATES]


def seed_pro_nas_hero_image(*, force: bool = False) -> str:
    """
    Ставить portrait на Page(slug=pro-nas).hero_image.

    За замовчуванням не перезаписує вже завантажене фото.
    Повертає короткий статус для stdout.
    """
    page = Page.objects.filter(slug='pro-nas').first()
    if page is None:
        return 'pro-nas page missing'

    if page.hero_image and not force:
        return f'hero_image already set ({page.hero_image.name})'

    source = next((p for p in _candidate_paths() if p.is_file()), None)
    if source is None:
        return 'no portrait file found (static/img/about/portrait.webp)'

    with source.open('rb') as fh:
        page.hero_image.save(source.name, File(fh), save=True)

    updates: list[str] = []
    if not page.hero_image_alt:
        page.hero_image_alt = _DEFAULT_ALT
        updates.append('hero_image_alt')
    if not page.hero_caption:
        page.hero_caption = _DEFAULT_CAPTION
        updates.append('hero_caption')
    if updates:
        page.save(update_fields=updates)

    return f'hero_image seeded from {source.name}'
