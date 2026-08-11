from src.blog.models import Post
from src.pages.models import Page
from src.seo.models import Redirect301
from src.services.models import Service


def iter_public_urls():
    yield {'loc': '/', 'lastmod': None}
    for page in Page.objects.filter(is_published=True).only('slug', 'updated_at'):
        yield {'loc': page.get_absolute_url(), 'lastmod': page.updated_at}
    yield {'loc': '/posluhy/', 'lastmod': None}
    for service in Service.objects.filter(is_published=True).only('slug', 'updated_at'):
        yield {'loc': service.get_absolute_url(), 'lastmod': service.updated_at}
    yield {'loc': '/blog/', 'lastmod': None}
    for post in Post.objects.filter(is_published=True).only('slug', 'updated_at', 'published_at'):
        yield {
            'loc': post.get_absolute_url(),
            'lastmod': post.updated_at or post.published_at,
        }


def get_active_redirect(path: str) -> Redirect301 | None:
    return Redirect301.objects.filter(old_path=path, is_active=True).first()


def build_robots_txt(absolute_sitemap: str, extra: str = '') -> str:
    lines = [
        'User-agent: *',
        'Disallow: /admin/',
        'Disallow: /leads/',
        f'Sitemap: {absolute_sitemap}',
    ]
    if extra.strip():
        lines.append(extra.strip())
    return '\n'.join(lines) + '\n'
