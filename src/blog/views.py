from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from src.blog.selectors import (
    FILTER_PILLS,
    api_key_from_db_slug,
    get_published_post,
    list_active_categories,
    list_blog_feed,
    list_posts,
    resolve_api_category,
    resolve_post_seo,
)


def _parse_page(raw: str | None) -> int:
    try:
        page = int(raw or '1')
    except (TypeError, ValueError):
        return 1
    return page if page >= 1 else 1


def _canonical_blog_url(api_key: str, page: int = 1) -> str:
    url = reverse('blog:list')
    params = []
    if api_key and api_key != 'all':
        _, db_slug = resolve_api_category(api_key)
        if db_slug:
            params.append(f'category={db_slug}')
    if page > 1:
        params.append(f'page={page}')
    if params:
        return f'{url}?{"&".join(params)}'
    return url


def _feed_context(api_category: str | None, page: int = 1) -> dict:
    feed = list_blog_feed(api_category=api_category, page=page)
    feed.update(
        {
            'filter_pills': FILTER_PILLS,
            'categories': list_active_categories(),
            'page_num': page,
        }
    )
    return feed


class PostListView(View):
    template_name = 'blog/list.html'

    def get(self, request):
        category = request.GET.get('category') or None
        page_num = _parse_page(request.GET.get('page'))
        if category in ('all', 'cases', 'news', 'tips'):
            api_key = category
        elif category:
            api_key = api_key_from_db_slug(category)
        else:
            api_key = 'all'
        ctx = _feed_context(api_key, page_num)
        ctx.update(
            {
                'page_title': 'Блог',
                'seo_title': 'Блог / кейси / новини',
                'seo_h1': 'Блог / Кейси / Новини',
                'seo_description': (
                    'Актуальна судова практика, розʼяснення Кодексу України '
                    'з процедур банкрутства та реальні історії списання боргів.'
                ),
            }
        )
        return render(request, self.template_name, ctx)


class PostListPartialView(View):
    """HTMX teaser для головної (збережено)."""

    teaser_template_name = 'blog/partials/teaser_grid.html'

    def get(self, request):
        if not request.headers.get('HX-Request'):
            q = request.GET.urlencode()
            url = reverse('blog:list')
            return HttpResponseRedirect(f'{url}?{q}' if q else url)

        category = request.GET.get('category') or None
        teaser = request.GET.get('teaser') == '1'
        page_num = _parse_page(request.GET.get('page'))

        if teaser:
            try:
                limit = int(request.GET.get('limit') or '3')
            except (TypeError, ValueError):
                limit = 3
            limit = max(1, min(limit, 12))
            posts = list(list_posts(category_slug=category, limit=limit))
            return render(
                request,
                self.teaser_template_name,
                {
                    'posts': posts,
                    'active_category': category or '',
                },
            )

        feed = _feed_context(api_key_from_db_slug(category), page_num)
        response = render(request, 'blog/partials/feed.html', feed)
        response['HX-Push-Url'] = _canonical_blog_url(feed['api_category'], page_num)
        return response


class ApiBlogFeedView(View):
    """GET /api/blog/{all|cases|news|tips}/ — заміна сітки фільтром."""

    template_name = 'blog/partials/feed.html'
    load_more_template = 'blog/partials/load_more.html'

    def get(self, request, api_category: str | None = None):
        key = api_category or request.GET.get('category') or 'all'
        key, _ = resolve_api_category(key)
        if not request.headers.get('HX-Request'):
            return HttpResponseRedirect(_canonical_blog_url(key, 1))

        page_num = _parse_page(request.GET.get('page'))
        ctx = _feed_context(key, page_num)
        feed_html = render(request, self.template_name, ctx).content.decode('utf-8')
        load_more = render(
            request,
            self.load_more_template,
            {**ctx, 'oob': True},
        ).content.decode('utf-8')
        response = HttpResponse(feed_html + load_more)
        response['HX-Push-Url'] = _canonical_blog_url(key, page_num)
        return response


class ApiBlogMoreView(View):
    """GET /api/blog/more?page=&category= — дописування карток."""

    cards_template = 'blog/partials/cards.html'
    load_more_template = 'blog/partials/load_more.html'

    def get(self, request):
        key = request.GET.get('category') or 'all'
        key, _ = resolve_api_category(key)
        page_num = _parse_page(request.GET.get('page'))
        if page_num < 2:
            page_num = 2

        if not request.headers.get('HX-Request'):
            return HttpResponseRedirect(_canonical_blog_url(key, page_num))

        ctx = _feed_context(key, page_num)
        cards = render(request, self.cards_template, ctx).content.decode('utf-8')
        load_more = render(
            request,
            self.load_more_template,
            {**ctx, 'oob': True},
        ).content.decode('utf-8')
        response = HttpResponse(cards + load_more)
        response['HX-Push-Url'] = _canonical_blog_url(key, page_num)
        return response


class PostDetailView(View):
    template_name = 'blog/detail.html'

    def get(self, request, slug):
        post = get_published_post(slug)
        if post is None:
            raise Http404
        share_url = request.build_absolute_uri(post.get_absolute_url())
        ctx = {
            'post': post,
            'share_url': share_url,
            **resolve_post_seo(post),
        }
        return render(request, self.template_name, ctx)
