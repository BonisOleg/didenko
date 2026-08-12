"""Seed зображень для advantages (SiteBlock) та обкладинок блогу з static/."""

from __future__ import annotations

from pathlib import Path

from django.conf import settings
from django.core.cache import cache
from django.core.files import File

from src.blog.models import Post
from src.pages.models_siteblock import SiteBlock

_ADVANTAGES_STATIC = ('static', 'img', 'home', 'advantages.webp')
_ADVANTAGES_MEDIA = ('media', 'blocks', 'advantages-didenko.jpg')

# slug посту → файл у static/img/blog/ (і fallback media/blog/)
_BLOG_COVERS: dict[str, tuple[tuple[str, ...], ...]] = {
    'keys-zakhyst-mayna': (
        ('static', 'img', 'blog', 'keys-zakhyst-mayna.webp'),
        ('media', 'blog', 'keys-zakhyst-mayna.jpg'),
    ),
    'keys-pryklad-1': (
        ('static', 'img', 'blog', 'keys-pryklad-1.webp'),
        ('media', 'blog', 'keys-pryklad-1.jpg'),
    ),
    'keys-pryklad-2': (
        ('static', 'img', 'blog', 'keys-pryklad-2.webp'),
        ('media', 'blog', 'keys-pryklad-2.jpg'),
    ),
    'novyna-kodeks': (
        ('static', 'img', 'blog', 'novyna-kodeks.webp'),
        ('media', 'blog', 'novyna-kodeks.jpg'),
    ),
    'porada-pidhotovka-dokumentiv': (
        ('static', 'img', 'blog', 'porada-pidhotovka-dokumentiv.webp'),
        ('media', 'blog', 'porada-pidhotovka-dokumentiv.jpg'),
    ),
}


def _base() -> Path:
    return Path(settings.BASE_DIR)


def _first_existing(candidates: tuple[tuple[str, ...], ...]) -> Path | None:
    for parts in candidates:
        path = _base().joinpath(*parts)
        if path.is_file():
            return path
    return None


def _assign_image(field, source: Path) -> None:
    with source.open('rb') as fh:
        field.save(source.name, File(fh), save=True)


def seed_advantages_image(*, force: bool = False) -> str:
    """SiteBlock home.advantages_image ← static/img/home/advantages.webp."""
    block, _ = SiteBlock.objects.get_or_create(
        page=SiteBlock.Page.HOME,
        key='advantages_image',
        defaults={
            'label': 'Фото під текстом',
            'content_type': SiteBlock.ContentType.IMAGE,
            'is_active': True,
            'sort_order': 50,
        },
    )
    if block.image and not force:
        name = block.image.name
        try:
            if Path(block.image.path).is_file():
                return f'advantages_image already set ({name})'
        except (ValueError, OSError):
            pass

    source = _first_existing((_ADVANTAGES_STATIC, _ADVANTAGES_MEDIA))
    if source is None:
        return 'no advantages image found'

    _assign_image(block.image, source)
    cache.delete(getattr(settings, 'SITE_BLOCKS_CACHE_KEY', 'didenko_site_blocks_v1'))
    return f'advantages_image seeded from {source.name}'


def seed_blog_covers(*, force: bool = False) -> list[str]:
    """Post.cover_image з static/img/blog/{slug}.webp для відомих slug."""
    lines: list[str] = []
    for slug, candidates in _BLOG_COVERS.items():
        post = Post.objects.filter(slug=slug).first()
        if post is None:
            lines.append(f'{slug}: post missing')
            continue
        if post.cover_image and not force:
            try:
                if Path(post.cover_image.path).is_file():
                    lines.append(f'{slug}: cover already set')
                    continue
            except (ValueError, OSError):
                pass
        source = _first_existing(candidates)
        if source is None:
            lines.append(f'{slug}: no cover file')
            continue
        _assign_image(post.cover_image, source)
        if not post.cover_alt:
            post.cover_alt = post.title[:255]
            post.save(update_fields=['cover_alt'])
        lines.append(f'{slug}: cover from {source.name}')
    return lines


def seed_demo_images(*, force: bool = False) -> list[str]:
    return [
        seed_advantages_image(force=force),
        *seed_blog_covers(force=force),
    ]
