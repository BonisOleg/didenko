from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from src.pages.admin_theme import theme_css

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('theme.css', theme_css, name='theme_css'),
    path('healthz/', TemplateView.as_view(template_name='seo/healthz.txt'), name='healthz'),
    path('', include('src.seo.urls')),
    path('', include('src.leads.urls')),
    path('', include('src.services.urls')),
    path('', include('src.blog.urls')),
    path('', include('src.pages.urls')),
]

handler404 = 'src.core.views.page_not_found'
handler500 = 'src.core.views.server_error'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
