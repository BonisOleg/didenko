from django.urls import path

from src.seo.views import RobotsTxtView, SitemapXmlView

app_name = 'seo'

urlpatterns = [
    path('sitemap.xml', SitemapXmlView.as_view(), name='sitemap'),
    path('robots.txt', RobotsTxtView.as_view(), name='robots'),
]
