"""Валідація фавіконки, завантаженої через адмінку."""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from django.db.models.fields.files import FieldFile
from PIL import Image, UnidentifiedImageError

FAVICON_MAX_BYTES = 512 * 1024  # 512 КБ
FAVICON_MAX_SIDE = 512  # px
FAVICON_ALLOWED_EXTENSIONS = frozenset({'png', 'ico', 'webp'})
FAVICON_ALLOWED_CONTENT_TYPES = frozenset({
    'image/png',
    'image/x-icon',
    'image/vnd.microsoft.icon',
    'image/webp',
    'image/ico',
})


def _extension(name: str) -> str:
    if not name or '.' not in name:
        return ''
    return name.rsplit('.', 1)[-1].lower().strip()


def validate_favicon_upload(file) -> None:
    """Перевіряє формат, розмір файлу та габарити зображення."""
    if not file:
        return

    # Уже збережені файли не перевіряємо повторно.
    if isinstance(file, FieldFile) and not isinstance(file, UploadedFile):
        return

    ext = _extension(getattr(file, 'name', '') or '')
    if ext not in FAVICON_ALLOWED_EXTENSIONS:
        raise ValidationError(
            'Невірний формат. Дозволені лише PNG, ICO або WEBP.',
            code='favicon_invalid_format',
        )

    content_type = (getattr(file, 'content_type', '') or '').lower()
    if content_type and content_type not in FAVICON_ALLOWED_CONTENT_TYPES:
        raise ValidationError(
            'Невірний тип файлу. Завантажте PNG, ICO або WEBP.',
            code='favicon_invalid_content_type',
        )

    size = getattr(file, 'size', None)
    if size is not None and size > FAVICON_MAX_BYTES:
        max_kb = FAVICON_MAX_BYTES // 1024
        raise ValidationError(
            f'Файл занадто великий. Максимум {max_kb} КБ.',
            code='favicon_too_large',
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
            code='favicon_unreadable',
        ) from exc
    except OSError as exc:
        raise ValidationError(
            'Пошкоджений файл зображення.',
            code='favicon_corrupt',
        ) from exc
    finally:
        try:
            file.seek(0)
        except Exception:
            pass

    if width > FAVICON_MAX_SIDE or height > FAVICON_MAX_SIDE:
        raise ValidationError(
            f'Зображення занадто велике. Максимум {FAVICON_MAX_SIDE}×{FAVICON_MAX_SIDE} px.',
            code='favicon_dimensions',
        )
