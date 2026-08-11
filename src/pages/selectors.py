"""Read-layer for pages / home."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.pages.models import HomeBlock, HomeHero, Page, SiteSettings


def get_site_settings() -> SiteSettings:
    return SiteSettings.load()


def get_home_hero() -> HomeHero | None:
    hero = HomeHero.load()
    if not hero.is_active:
        return None
    return hero


def list_visible_home_blocks():
    return list(
        HomeBlock.objects.filter(is_visible=True).order_by('sort_order', 'id'),
    )


def get_published_page(slug: str) -> Page | None:
    return Page.objects.filter(slug=slug, is_published=True).first()


@dataclass
class ResolvedBlock:
    block: HomeBlock
    items: Any = None
    skip: bool = False


def _resolve_block(block: HomeBlock) -> ResolvedBlock:
    payload = block.payload or {}
    btype = block.block_type

    if btype == HomeBlock.BlockType.SERVICES_TEASER:
        from src.services.selectors import list_published_services

        limit = int(payload.get('limit') or 6)
        items = list(list_published_services(limit=limit))
        return ResolvedBlock(block=block, items=items, skip=not items)

    if btype == HomeBlock.BlockType.BLOG_TEASER:
        from src.blog.selectors import list_posts

        limit = int(payload.get('limit') or 3)
        category_slug = payload.get('category_slug') or None
        items = list(
            list_posts(category_slug=category_slug, limit=limit),
        )
        return ResolvedBlock(block=block, items=items, skip=not items)

    if btype == HomeBlock.BlockType.ADVANTAGES:
        items = payload.get('items') or []
        return ResolvedBlock(block=block, items=items, skip=not items)

    if btype == HomeBlock.BlockType.AUDIENCE:
        items = payload.get('items') or []
        return ResolvedBlock(block=block, items=items, skip=not items)

    if btype == HomeBlock.BlockType.LEAD_FORM:
        return ResolvedBlock(block=block, items=payload, skip=False)

    return ResolvedBlock(block=block, skip=True)


def get_home_context() -> dict:
    hero = get_home_hero()
    resolved = []
    for block in list_visible_home_blocks():
        rb = _resolve_block(block)
        if not rb.skip:
            resolved.append(rb)

    from src.blog.selectors import list_active_categories
    from src.pages.block_render import get_block_text

    headline = get_block_text('home', 'hero_title') or (
        hero.headline if hero else 'Діденко'
    )
    sub = get_block_text('home', 'hero_sub') or (
        hero.subheadline if hero and hero.subheadline else ''
    )

    return {
        'hero': hero,
        'home_blocks': resolved,
        'blog_categories': list(list_active_categories()),
        'page_title': headline,
        'seo_title': headline,
        'seo_description': sub[:160] if sub else '',
        'seo_h1': headline,
    }


def resolve_page_seo(page: Page) -> dict:
    return {
        'page_title': page.seo_title or page.title,
        'seo_title': page.seo_title or page.title,
        'seo_description': page.seo_description or '',
        'seo_h1': page.seo_h1 or page.title,
    }
