"""Валідація фото hero сторінки «Про мене»."""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from django.db.models.fields.files import FieldFile
from PIL import Image, UnidentifiedImageError

ABOUT_HERO_MAX_BYTES = 1 * 1024 * 1024  # 1 МБ
ABOUT_HERO_MIN_WIDTH = 480
ABOUT_HERO_MIN_HEIGHT = 600
ABOUT_HERO_RECOMMENDED = (800, 1000)
ABOUT_HERO_ASPECT = 4 / 5  # ширина / висота
ABOUT_HERO_ASPECT_TOLERANCE = 0.10  # ±10%
ABOUT_HERO_ALLOWED_EXTENSIONS = frozenset({'jpg', 'jpeg', 'png', 'webp'})
ABOUT_HERO_ALLOWED_CONTENT_TYPES = frozenset({
    'image/jpeg',
    'image/jpg',
    'image/pjpeg',
    'image/png',
    'image/webp',
})

ABOUT_HERO_HELP_TEXT = (
    'Формат: JPG, PNG або WebP. Рекомендований розмір 800×1000 px '
    '(співвідношення 4:5). Мінімум 480×600 px. Файл до 1 МБ. '
    'Відхилення від 4:5 — не більше 10%.'
)


def _extension(name: str) -> str:
    if not name or '.' not in name:
        return ''
    return name.rsplit('.', 1)[-1].lower().strip()


def validate_about_hero_image(file) -> None:
    """Перевіряє формат, розмір файлу, габарити та співвідношення 4:5."""
    if not file:
        return

    if isinstance(file, FieldFile) and not isinstance(file, UploadedFile):
        return

    ext = _extension(getattr(file, 'name', '') or '')
    if ext not in ABOUT_HERO_ALLOWED_EXTENSIONS:
        raise ValidationError(
            'Невірний формат. Дозволені лише JPG, PNG або WebP.',
            code='about_hero_invalid_format',
        )

    content_type = (getattr(file, 'content_type', '') or '').lower()
    if content_type and content_type not in ABOUT_HERO_ALLOWED_CONTENT_TYPES:
        raise ValidationError(
            'Невірний тип файлу. Завантажте JPG, PNG або WebP.',
            code='about_hero_invalid_content_type',
        )

    size = getattr(file, 'size', None)
    if size is not None and size > ABOUT_HERO_MAX_BYTES:
        raise ValidationError(
            'Файл занадто великий. Максимум 1 МБ.',
            code='about_hero_too_large',
        )

    width = height = 0
    try:
        file.seek(0)
        with Image.open(file) as image:
            image.verify()
        file.seek(0)
        with Image.open(file) as image:
            width, height = image.size
    except UnidentifiedImageError as exc:
        raise ValidationError(
            'Не вдалося прочитати зображення. Перевірте формат файлу.',
            code='about_hero_unreadable',
        ) from exc
    except OSError as exc:
        raise ValidationError(
            'Пошкоджений файл зображення.',
            code='about_hero_corrupt',
        ) from exc
    finally:
        try:
            file.seek(0)
        except Exception:
            pass

    if width < ABOUT_HERO_MIN_WIDTH or height < ABOUT_HERO_MIN_HEIGHT:
        raise ValidationError(
            f'Зображення занадто мале. Мінімум '
            f'{ABOUT_HERO_MIN_WIDTH}×{ABOUT_HERO_MIN_HEIGHT} px '
            f'(рекомендовано {ABOUT_HERO_RECOMMENDED[0]}×{ABOUT_HERO_RECOMMENDED[1]} px).',
            code='about_hero_too_small',
        )

    ratio = width / height if height else 0
    low = ABOUT_HERO_ASPECT * (1 - ABOUT_HERO_ASPECT_TOLERANCE)
    high = ABOUT_HERO_ASPECT * (1 + ABOUT_HERO_ASPECT_TOLERANCE)
    if ratio < low or ratio > high:
        raise ValidationError(
            'Невірне співвідношення сторін. Потрібно 4:5 '
            f'(наприклад {ABOUT_HERO_RECOMMENDED[0]}×{ABOUT_HERO_RECOMMENDED[1]} px), '
            'допустиме відхилення ±10%.',
            code='about_hero_bad_aspect',
        )
