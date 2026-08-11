from django.core.paginator import Paginator
from django.utils import timezone

from src.blog.models import Category, Post

POSTS_PER_PAGE = 9

# API keys (ТЗ) → DB slug (сумісність з home teaser)
API_CATEGORY_MAP = {
    'all': None,
    'cases': 'keysy',
    'news': 'novyny',
    'tips': 'porady',
}

FILTER_PILLS = (
    ('all', 'Усі матеріали'),
    ('cases', 'Реальні кейси'),
    ('news', 'Новини та законодавство'),
    ('tips', 'Поради арбітражної керуючої'),
)

CATEGORY_BADGE = {
    'keysy': 'Кейси',
    'novyny': 'Новини',
    'porady': 'Поради',
}

READ_MORE_LABEL = {
    'keysy': 'Читати кейс',
    'novyny': 'Читати статтю',
    'porady': 'Читати матеріали',
}


def list_active_categories():
    return Category.objects.filter(is_active=True).order_by('sort_order', 'id')


def published_posts_qs():
    return (
        Post.objects.filter(
            is_published=True,
            published_at__lte=timezone.now(),
        )
        .select_related('category')
        .order_by('-published_at', '-id')
    )


def resolve_api_category(raw: str | None) -> tuple[str, str | None]:
    key = (raw or 'all').strip().lower()
    if key not in API_CATEGORY_MAP:
        key = 'all'
    return key, API_CATEGORY_MAP[key]


def api_key_from_db_slug(slug: str | None) -> str:
    if not slug:
        return 'all'
    for key, db_slug in API_CATEGORY_MAP.items():
        if db_slug == slug:
            return key
    return 'all'


def list_posts(
    *,
    category_slug: str | None = None,
    page: int = 1,
    per_page: int = POSTS_PER_PAGE,
    limit: int | None = None,
    exclude_ids: list[int] | None = None,
):
    qs = published_posts_qs()
    if category_slug:
        cat = Category.objects.filter(slug=category_slug, is_active=True).first()
        if cat:
            qs = qs.filter(category=cat)
    if exclude_ids:
        qs = qs.exclude(pk__in=exclude_ids)
    if limit is not None:
        return qs[:limit]
    paginator = Paginator(qs, per_page)
    return paginator.get_page(page)


def get_featured_post(*, category_slug: str | None = None) -> Post | None:
    qs = published_posts_qs().filter(is_featured=True)
    if category_slug:
        qs = qs.filter(category__slug=category_slug)
    return qs.first()


def list_blog_feed(*, api_category: str | None = None, page: int = 1):
    api_key, db_slug = resolve_api_category(api_category)
    featured_candidate = get_featured_post(category_slug=db_slug)
    exclude_ids = [featured_candidate.pk] if featured_candidate else None
    page_obj = list_posts(
        category_slug=db_slug,
        page=page,
        exclude_ids=exclude_ids,
    )
    featured = featured_candidate if page == 1 else None
    return {
        'api_category': api_key,
        'active_category': db_slug or '',
        'featured_post': featured,
        'page_obj': page_obj,
        'show_featured': bool(featured),
    }


def post_badge_label(post: Post) -> str:
    if post.is_featured:
        return 'Головний кейс'
    slug = post.category.slug if post.category else ''
    return CATEGORY_BADGE.get(slug, post.category.title if post.category else 'Матеріал')


def post_read_more_label(post: Post) -> str:
    if post.is_featured:
        return 'Читати повний кейс'
    slug = post.category.slug if post.category else ''
    return READ_MORE_LABEL.get(slug, 'Читати матеріали')


def get_published_post(slug: str) -> Post | None:
    return published_posts_qs().filter(slug=slug).first()


def resolve_post_seo(post: Post) -> dict:
    return {
        'page_title': post.seo_title or post.title,
        'seo_title': post.seo_title or post.title,
        'seo_description': post.seo_description or post.excerpt,
        'seo_h1': post.seo_h1 or post.title,
    }
