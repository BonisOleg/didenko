from django.http import HttpResponse
from django.views import View

from src.pages.selectors import get_site_settings
from src.seo.selectors import build_robots_txt, iter_public_urls


class SitemapXmlView(View):
    def get(self, request):
        base = request.build_absolute_uri('/').rstrip('/')
        lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        ]
        for item in iter_public_urls():
            loc = item['loc']
            if not loc.startswith('http'):
                loc = f'{base}{loc}'
            lines.append('<url>')
            lines.append(f'<loc>{loc}</loc>')
            if item.get('lastmod'):
                lines.append(f'<lastmod>{item["lastmod"].date().isoformat()}</lastmod>')
            lines.append('</url>')
        lines.append('</urlset>')
        return HttpResponse('\n'.join(lines), content_type='application/xml')


class RobotsTxtView(View):
    def get(self, request):
        settings_obj = get_site_settings()
        sitemap = request.build_absolute_uri('/sitemap.xml')
        body = build_robots_txt(sitemap, settings_obj.robots_extra or '')
        return HttpResponse(body, content_type='text/plain')
